from django.urls import path

from .views import Checkout, VerifyPayment

urlpatterns = [
    path("checkout/", Checkout.as_view()),
    path("verifypayment/", VerifyPayment.as_view()),
]
