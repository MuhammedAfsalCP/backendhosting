from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Products
from users.serializer import User

from .models import Order, OrderItem
from .serializer import (AllOrderSerializer, OrderItemSerializer,
                         OrderSerializer)


# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderView(ListAPIView):

    pagination_class = ProductPagination
    serializer_class = OrderSerializer

    def get_queryset(self):

        user = self.request.user
        return Order.objects.filter(user=user)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class OrderUpdate(APIView):

    def put(self, request, pk):
        print(request)
        action = request.data.get("method")
        print(action)
        try:

            product = OrderItem.objects.get(Q(id=pk) & ~Q(status="Cancelled"))

        except:
            return Response("invalid Product", status=status.HTTP_400_BAD_REQUEST)
        if action == "Cancelled":
            product.status = "Cancelled"
            product.save()
            return Response("updated", status=status.HTTP_202_ACCEPTED)
        elif action == "Returned":
            product.status = "Returned"
            product.save()
            return Response("updated", status=status.HTTP_202_ACCEPTED)


class allorder(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        order = Order.objects.all()
        serializer = AllOrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class Specificorder(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            orderitem = Order.objects.get(id=pk)
        except:
            return Response("invalidProduct", status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(orderitem, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk):
        action = request.data.get("method")
        print(action)
        try:

            orderitems = OrderItem.objects.filter(
                Q(order__id=pk) & ~Q(status="Cancelled")
            )
            print(orderitems)

        except:
            return Response("invalid Product", status=status.HTTP_400_BAD_REQUEST)
        if action == "Delivered":
            orderitems.update(status="Delivered")
            return Response("updated", status=status.HTTP_202_ACCEPTED)


class TotalPayment(APIView):
    def get(self, request):

        total_orders = Order.objects.filter(items__status="Delivered")

        users = User.objects.filter(Q(is_staff=False) & Q(is_deleted=False))
        total_revenue = sum(order.total_price for order in total_orders)
        orders = Order.objects.all()
        products = Products.objects.filter(is_deleted=False)

        print(total_revenue)

        return Response(
            {
                "totalrevanue": total_revenue,
                "userlength": len(users),
                "orderlen": len(orders),
                "productlen": len(products),
            },
            status=status.HTTP_200_OK,
        )
