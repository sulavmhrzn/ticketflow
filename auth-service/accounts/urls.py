from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import RegisterView, ResendOTPView, VerifyPhoneView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("verify-phone/", VerifyPhoneView.as_view(), name="verify-phone"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend_otp"),
]
