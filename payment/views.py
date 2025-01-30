import razorpay
from decouple import config
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem


class Checkout(APIView):
    def post(self, request):
        # Fetch user cart items and address
        cartitems = CartItem.objects.filter(cart__user=request.user)

        # Calculate total price
        total_price = sum(item.product.Price * item.quantity for item in cartitems)
        total_price_paise = int(total_price * 100)  # Convert to paise

        client = razorpay.Client(
            auth=(config("Razerpay_KeyId"), config("Razerpay_KeySecret"))
        )

        # Create Razorpay payment order
        payment = client.order.create(
            {"amount": total_price_paise, "currency": "INR", "payment_capture": 1}
        )

        response_data = {
            "payment_id": payment["id"],
            "amount": total_price_paise,
            "currency": "INR",
            "message": "Order created. Complete payment using Razorpay.",
        }

        # Send payment details to frontend
        return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyPayment(APIView):
    def post(self, request):
        razorpay_payment_id = request.data.get("payment_id")
        razorpay_order_id = request.data.get("order_id")
        razorpay_signature = request.data.get("signature")

        client = razorpay.Client(
            auth=(config("Razerpay_KeyId"), config("Razerpay_KeySecret"))
        )

        try:
            # Verify Razorpay payment signature
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )
            address = request.data.get("address")
            print(address)
            # Start a transaction
            with transaction.atomic():
                # Create the order in the database only after payment verification
                cartitems = CartItem.objects.filter(cart__user=request.user)
                address = request.data.get(
                    "address"
                )  # You should get the address here as well

                total_price = sum(
                    item.product.Price * item.quantity for item in cartitems
                )

                # Create order in the database
                order = Order.objects.create(
                    user=request.user,
                    order_id=razorpay_order_id,
                    address=address,
                    total_price=total_price,
                    # Mark as paid when payment is verified
                )

                # Bulk create order items
                order_items = [
                    OrderItem(order=order, product=item.product, quantity=item.quantity)
                    for item in cartitems
                ]
                OrderItem.objects.bulk_create(order_items)

                # Update product stock
                for item in cartitems:
                    product = item.product
                    product.Stock -= item.quantity
                    product.save()

                # Clear cart items after successful payment
                cart = Cart.objects.filter(user=request.user)
                cart.delete()
                cartitems.delete()

            return Response(
                {"success": "Payment verified and order completed"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # If payment verification fails, roll back the transaction and do not create the order
            return Response(
                {"error": f"Payment verification failed: {str(e)}"}, status=400
            )
