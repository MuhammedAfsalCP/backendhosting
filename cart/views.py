from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serialzer import CartItemSerializer, CartSerializer

# Create your views here.


class CartAdd(CreateAPIView, ListAPIView):

    def get_serializer_class(self):

        if self.request.method == "GET":
            return CartSerializer
        return CartItemSerializer

    def create(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        cart, created = Cart.objects.get_or_create(user=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("hi")
        product = serializer.validated_data["product"]
        quantity = 1
        if product.Stock >= quantity:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            if not created:
                if product.Stock >= cart_item.quantity:
                    cart_item.quantity += quantity
                    cart_item.save()
                    return Response(
                        {"messege": "Item Already Added ,Quantity Increased"},
                        status=status.HTTP_200_OK,
                    )
                return Response("Out Of Stock", status=status.HTTP_400_BAD_REQUEST)

            cart_item.quantity = quantity
            cart_item.save()
            return Response(
                {"messege": "successfully added"}, status=status.HTTP_201_CREATED
            )
        return Response("Out Of Stock", status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        user = self.request.user
        return Cart.objects.filter(user=user)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartDelete(APIView):

    def get(self, request, pk):
        try:
            user = self.request.user
            print(user)
            cart_item = CartItem.objects.get(Q(id=pk) & Q(cart__user=user))

        except CartItem.DoesNotExist:
            return Response("cart not found", status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(id=pk)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item.delete()
        return Response("item Deleted", status=status.HTTP_200_OK)

    def put(self, request, pk):
        print(request)
        try:
            action = request.data.get("method")
            print(action)
        except:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        if action == "increase":
            cart_item = CartItem.objects.get(id=pk)
            if cart_item.product.Stock >= cart_item.quantity + 1:
                cart_item.quantity += 1
                cart_item.save()
                return Response("Quantity Increased", status=status.HTTP_201_CREATED)
            else:
                return Response("Out Of Stock", status=status.HTTP_400_BAD_REQUEST)

        elif action == "decrease":
            cart_item = CartItem.objects.get(id=pk)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1

                cart_item.save()
                return Response("Quantity Decreased", status=status.HTTP_201_CREATED)
            else:
                cart_item.delete()
                return Response("product Deleted", status=status.HTTP_200_OK)
