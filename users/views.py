import random

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializer import (AdminShowSerializer, LoginSerializer,
                         UserAllDetailsSerializer, UserRegisterSerializer,
                         UserVerificatioSerializer)

# Create your views here.

otp_store = {}


class UserDetails(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            otp = "".join(str(random.randint(0, 9)) for _ in range(6))  # Generate OTP
            print(otp)

            username = request.data.get("username")
            email = request.data.get("email")

            if email:
                try:
                    # Create an EmailMessage instance
                    subject = "Your OTP Code"
                    message = f"Your OTP code for verification is: {otp}"
                    from_email = settings.EMAIL_HOST_USER  # Default from email
                    to_email = [email]

                    # Send the email
                    email = EmailMessage(subject, message, from_email, to_email)
                    email.send()

                    # Store OTP only after successful email send
                    otp_store[username] = otp
                    print(f"OTP sent to {email}: {otp}")

                    return Response(
                        {"message": "OTP Successfully Sent"},
                        status=status.HTTP_201_CREATED,
                    )

                except Exception as e:
                    print(f"Error sending email: {e}")
                    return Response(
                        {"error": "Failed to send OTP email."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            else:
                return Response(
                    {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class otpVerification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp = request.data.get("otp")
        username = request.data.get("username")

        if username not in otp_store:
            return Response(
                {"error": "Invalid request. No OTP sent to this username."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Compare the received OTP with the stored OTP
        stored_otp = otp_store[username]
        print(f"Stored OTP: {stored_otp}")

        if otp == stored_otp:
            del otp_store[username]

            verification_serializer = UserVerificatioSerializer(data=request.data)
            if verification_serializer.is_valid():
                verification_serializer.save()

            return Response(
                {"message": "OTP verification successful."}, status=status.HTTP_200_OK
            )
        else:
            # OTP doesn't match
            return Response(
                {"error": "Invalid OTP. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            userdetail = User.objects.get(username=username)
            serializer = LoginSerializer(userdetail)
            return Response(
                {
                    "access": access_token,
                    "refresh": str(refresh),
                    "userdetail": serializer.data,
                }
            )
        else:

            return Response(
                {"error": "invaliduser"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserDetailsView(APIView):

    def get(self, request):
        user = request.user  # `request.user` is populated by JWTAuthentication
        return Response(
            {"userdetail": {"username": user.username, "is_staff": user.is_staff}}
        )


class TotalUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(Q(is_staff=False) & Q(is_deleted=False))

        serializer = AdminShowSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class SpesificUser(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        print(request)
        try:
            action = request.data.get("method")
            print(action)
        except:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        if action == "Block":
            user = User.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response("Blocked", status=status.HTTP_202_ACCEPTED)

        elif action == "Unblock":
            user = User.objects.get(id=pk)
            user.is_active = True
            user.save()
            return Response("UnBlocked", status=status.HTTP_202_ACCEPTED)


class useralldetails(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserAllDetailsSerializer(user, context={"request": request})
        return Response(serializer.data)
