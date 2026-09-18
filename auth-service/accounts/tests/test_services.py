from datetime import timedelta

import pytest
from django.utils import timezone

from accounts.models import PhoneOTP
from accounts.services import generate_otp, verify_otp
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_verify_otp_succeeds_with_correct_code():
    user = UserFactory(is_phone_verified=False)
    code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)
    result = verify_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION, code=code)

    assert result is True
    user.refresh_from_db()
    assert user.is_phone_verified is True


@pytest.mark.django_db
def test_verify_otp_rejects_wrong_code():
    user = UserFactory(is_phone_verified=False)
    generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)

    result = verify_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION, code="000000")

    assert result is False
    user.refresh_from_db()
    assert user.is_phone_verified is False


@pytest.mark.django_db
def test_verify_otp_rejects_expired_code():
    user = UserFactory(is_phone_verified=False)
    code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)

    # Directly manipulate expiry rather than sleeping 5 real minutes in a test
    otp = PhoneOTP.objects.get(user=user)
    otp.expires_at = timezone.now() - timedelta(seconds=1)
    otp.save(update_fields=["expires_at"])

    result = verify_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION, code=code)

    assert result is False


@pytest.mark.django_db
def test_generate_otp_invalidates_previous_unused_otp():
    user = UserFactory()
    old_code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)
    new_code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)

    assert (
        verify_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION, code=old_code)
        is False
    )
    assert (
        verify_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION, code=new_code)
        is True
    )
