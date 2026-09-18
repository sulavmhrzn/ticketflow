from accounts.models import User


def get_user_by_phone_number(*, phone_number: str) -> User | None:
    return User.objects.filter(phone_number=phone_number).first()
