import factory
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("phone_number",)
        skip_postgeneration_save = True

    phone_number = factory.Sequence(lambda n: f"+97798{n:08d}")
    first_name = "Test"
    last_name = "User"
    role = User.Role.CUSTOMER
    is_phone_verified = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw_password = extracted or "testpass123"
        self.set_password(raw_password)
        if create:
            self.save()
