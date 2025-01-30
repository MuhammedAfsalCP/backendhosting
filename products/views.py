from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .utils import upload_image_to_s3
from .models import Products
from .serializer import ProductsSeriealizer
from rest_framework import status
# Create your views here.


class ProductPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


from rest_framework.permissions import AllowAny, IsAdminUser


class ProductDetails(ModelViewSet):
    queryset = Products.objects.filter(is_deleted=False)
    serializer_class = ProductsSeriealizer
    pagination_class = ProductPagination

    def get_permissions(self):

        if self.request.method in ["PUT", "POST", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
        
    

class ProductCategory(APIView):
    permission_classes = [AllowAny]

    def get(self, request, ctg):
        print(ctg)
        products = Products.objects.filter(Q(Category=ctg) & Q(is_deleted=False))

        if not products:
            return Response("Invalid Category")
        else:
            # Use the correct serializer here
            serializer = ProductsSeriealizer(
                products, many=True, context={"request": request}
            )
            return Response(serializer.data)


class Productfilter(APIView):
    permission_classes = [AllowAny]

    def get(self, request, flt):
        try:
            products = Products.objects.filter(
                Q(Name__icontains=flt) & Q(is_deleted=False)
            )
        except:
            return Response("Invalid product")

        serializer = ProductsSeriealizer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class offerProduct(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            products = Products.objects.get(id=2)
            print(products)
        except:
            return Response("Invalid product")

        print(products)
        serializer = ProductsSeriealizer(products, context={"request": request})
        return Response(serializer.data)
