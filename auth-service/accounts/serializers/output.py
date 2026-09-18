from accounts.models import User
from rest_framework import serializers


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        ]
