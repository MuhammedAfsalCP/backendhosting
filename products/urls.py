# urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductCategory, ProductDetails, Productfilter, offerProduct

router = DefaultRouter()
router.register("productdetails", ProductDetails)

urlpatterns = [
    path("productcategory/<str:ctg>/", ProductCategory.as_view()),
    path("productfilter/<str:flt>/", Productfilter.as_view()),
    path("offerproduct/", offerProduct.as_view()),
] + router.urls

# Serve media files during development when DEBUG is True
