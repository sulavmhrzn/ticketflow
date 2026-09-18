from accounts.models import User, validate_nepali_phone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators=[
            validate_nepali_phone,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.ChoiceField(choices=[User.Role.CUSTOMER, User.Role.ORGANIZER])


class LoginInputSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["phone_number"] = user.phone_number
        token["is_phone_verified"] = user.is_phone_verified
        return token


class VerifyOTPInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=6, min_length=6)


class ResendOTPInputSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
