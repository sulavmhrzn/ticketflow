import json

from cryptography.hazmat.primitives import serialization
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from jwt.algorithms import RSAAlgorithm
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import PhoneOTP
from accounts.selectors import get_user_by_phone_number
from accounts.serializers.input import (
    RegisterInputSerializer,
    ResendOTPInputSerializer,
    VerifyOTPInputSerializer,
)
from accounts.serializers.output import UserOutputSerializer
from accounts.services import generate_otp, register_user, verify_otp
from accounts.tasks import send_otp_sms
from accounts.throttles import PhoneNumberRateThrottle


class RegisterView(APIView):
    def post(self, request):
        input_serializer = RegisterInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = register_user(**input_serializer.validated_data)

        return Response(UserOutputSerializer(user).data, status=201)


class VerifyPhoneView(APIView):
    def post(self, request):
        input_serializer = VerifyOTPInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = get_user_by_phone_number(
            phone_number=input_serializer.validated_data["phone_number"]
        )
        if user is None:
            return Response({"detail": "Invalid phone number or code"}, status=400)

        success = verify_otp(
            user=user,
            purpose=PhoneOTP.Purpose.REGISTRATION,
            code=input_serializer.validated_data["code"],
        )
        if not success:
            return Response({"detail": "Invalid phone number or code."}, status=400)

        return Response({"detail": "Phone verified successfully."}, status=200)


class ResendOTPView(APIView):
    throttle_classes = [PhoneNumberRateThrottle]
    throttle_scope = "resend_otp"

    def post(self, request):
        input_serializer = ResendOTPInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = get_user_by_phone_number(
            phone_number=input_serializer.validated_data["phone_number"]
        )

        if user is not None and not user.is_phone_verified:
            code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)
            send_otp_sms.delay(
                phone_number=user.phone_number,
                code=code,
                purpose=PhoneOTP.Purpose.REGISTRATION,
            )

        return Response(
            {
                "detail": "If this phone number is registered and unverified, a new code has been sent."
            },
            status=200,
        )


class JWKSView(View):
    def get(self, request):
        public_key_pem = (settings.BASE_DIR / "keys" / "public.pem").read_text()
        public_key = serialization.load_pem_public_key(public_key_pem.encode())

        jwk_json = json.loads(RSAAlgorithm.to_jwk(public_key))
        jwk_json["use"] = "sig"
        jwk_json["alg"] = "RS256"
        jwk_json["kid"] = "auth-key-1"
        return JsonResponse({"keys": [jwk_json]})
