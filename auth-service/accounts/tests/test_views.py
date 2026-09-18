import pytest
from rest_framework.test import APIClient

from accounts.models import PhoneOTP
from accounts.services import generate_otp
from accounts.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_creates_unverified_user_and_returns_201(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "phone_number": "+9779841234567",
            "first_name": "New",
            "last_name": "User",
            "password": "testpass123",
            "role": "customer",
        },
    )

    assert response.status_code == 201
    assert response.data["phone_number"] == "+9779841234567"
    assert "password " not in response.data


@pytest.mark.django_db
def test_register_rejects_invalid_phone_format(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "phone_number": "9841234567",
            "first_name": "New",
            "last_name": "User",
            "password": "testpass123",
            "role": "customer",
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_rejects_duplicate_phone_number(api_client):
    UserFactory(phone_number="+9779841234567")

    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "phone_number": "+9779841234567",
            "first_name": "New",
            "last_name": "User",
            "password": "testpass123",
            "role": "customer",
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_rejects_admin_role(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "phone_number": "+9779841234567",
            "first_name": "New",
            "last_name": "User",
            "password": "testpass123",
            "role": "admin",
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_returns_tokens_with_correct_claims(api_client):
    UserFactory(
        phone_number="+9779841234567",
        password="testpass123",
        role="organizer",
        is_phone_verified=True,
    )

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "phone_number": "+9779841234567",
            "password": "testpass123",
        },
    )

    assert response.status_code == 200
    assert "access" in response.data

    import jwt

    payload = jwt.decode(response.data["access"], options={"verify_signature": False})
    assert payload["role"] == "organizer"
    assert payload["is_phone_verified"] is True


@pytest.mark.django_db
def test_login_rejects_wrong_password(api_client):
    UserFactory(phone_number="+9779841234567", password="testpass123")

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "phone_number": "+9779841234567",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_verify_phone_succeeds_with_correct_code(api_client):
    user = UserFactory(is_phone_verified=False)
    code = generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)

    response = api_client.post(
        "/api/v1/auth/verify-phone/",
        {
            "phone_number": user.phone_number,
            "code": code,
        },
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_phone_verified is True


@pytest.mark.django_db
def test_verify_phone_rejects_wrong_code(api_client):
    user = UserFactory(is_phone_verified=False)
    generate_otp(user=user, purpose=PhoneOTP.Purpose.REGISTRATION)

    response = api_client.post(
        "/api/v1/auth/verify-phone/",
        {
            "phone_number": user.phone_number,
            "code": "000000",
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_resend_otp_returns_generic_response_regardless_of_user_existence(api_client):
    # Real user
    real_response = api_client.post(
        "/api/v1/auth/resend-otp/", {"phone_number": "+9779841234567"}
    )
    # Nonexistent user
    fake_response = api_client.post(
        "/api/v1/auth/resend-otp/", {"phone_number": "+9779849999999"}
    )

    assert real_response.status_code == fake_response.status_code == 200
    assert real_response.data == fake_response.data
