from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, LoginSerializer, LogoutSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=["POST"], detail=False)
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        phone_number = serializer.validated_data["phone_number"]
        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"status": 409, "message": "Username already exist"},
                status=status.HTTP_409_CONFLICT,
            )

        user = CustomUser.objects.create(
            username=username, email=email, password=make_password(password), phone_number=phone_number
        )
        user.save()
        return Response(
            {
                "status": 201,
                "message": "Signedup Successfully",
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @action(methods=["POST"], detail=False)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        try:
            user = authenticate(request, username=username, password=password)
            loggedUser = CustomUser.objects.get(username=username)
            if user is not None:
                login(request, user)
                custom_token = CustomTokenObtainPairView.serializer_class.get_token(user=user)
                token = {
                    "refresh": str(custom_token),
                    "access": str(custom_token.access_token),
                }
                return Response(
                    {
                        "status": 200,
                        "message": "LoggedIn Successfully",
                        "id": loggedUser.id,
                        "username": loggedUser.username,
                        "email": loggedUser.email,
                        "token": token,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": 401, "message": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"status": 404, "message": "username or password is incorrect"}, status=status.HTTP_404_NOT_FOUND
            )


# LOGOUT VIEW ( EXPIRES TOKEN )
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "You are loggedout "}, status=status.HTTP_200_OK)
