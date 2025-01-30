from django.urls import path

from .views import (Login, SpesificUser, TotalUsers, UserDetails,
                    UserDetailsView, otpVerification, useralldetails)

urlpatterns = [
    path("register/", UserDetails.as_view()),
    path("otpverification/", otpVerification.as_view()),
    path("userdetailsview/", UserDetailsView.as_view()),
    path("login/", Login.as_view()),
    path("userdetails/", TotalUsers.as_view()),
    path("edituser/<int:pk>/", SpesificUser.as_view()),
    path("spesificalldetails/<int:pk>/", useralldetails.as_view()),
]
