from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "phone_number"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad token")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token
