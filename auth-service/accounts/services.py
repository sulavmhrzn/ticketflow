import secrets
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from accounts.models import PhoneOTP, User
from accounts.tasks import send_otp_sms


def register_user(
    *,
    phone_number: str,
    first_name: str,
    last_name: str,
    password: str,
    role: str = User.Role.CUSTOMER,
) -> User:
    user = User.objects.create_user(
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=role,
    )
    code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)
    send_otp_sms.delay(
        phone_number=user.phone_number, code=code, purpose=PhoneOTP.Purpose.REGISTRATION
    )
    return user


def generate_otp(*, user: User, purpose: str) -> str:
    PhoneOTP.objects.filter(user=user, purpose=purpose, is_used=False).update(
        is_used=True
    )
    raw_code = f"{secrets.randbelow(1_000_000):06d}"
    PhoneOTP.objects.create(
        user=user,
        purpose=purpose,
        code_hash=make_password(raw_code),
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    return raw_code


def verify_otp(*, user: User, purpose: str, code: str) -> bool:
    otp = (
        PhoneOTP.objects.filter(user=user, purpose=purpose, is_used=False)
        .order_by("-created_at")
        .first()
    )

    if otp is None or not otp.is_valid() or not check_password(code, otp.code_hash):
        return False

    otp.is_used = True
    otp.save(update_fields=["is_used"])

    if purpose == PhoneOTP.Purpose.REGISTRATION:
        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified"])

    return True
