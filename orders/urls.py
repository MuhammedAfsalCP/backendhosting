from django.urls import path

from .views import (OrderUpdate, OrderView, Specificorder, TotalPayment,
                    allorder)

urlpatterns = [
    path("orderview/", OrderView.as_view()),
    path("orderupdate/<int:pk>/", OrderUpdate.as_view()),
    path("allorder/", allorder.as_view()),
    path("sepecificorder/<int:pk>/", Specificorder.as_view()),
    path("totalpayment/", TotalPayment.as_view()),
]
