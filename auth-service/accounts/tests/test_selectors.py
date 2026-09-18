import pytest

from accounts.selectors import get_user_by_phone_number
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_get_user_by_phone_number_returns_matching_user():
    user = UserFactory(phone_number="+9779841111111")
    result = get_user_by_phone_number(phone_number="+9779841111111")

    assert result == user


@pytest.mark.django_db
def test_get_user_by_phone_number_returns_none_when_not_found():
    result = get_user_by_phone_number(phone_number="+9779849999999")

    assert result is None
