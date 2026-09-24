from rest_framework_simplejwt.authentication import JWTAuthentication


class ClaimsBasedUser:
    def __init__(self, token):
        self.id = token["user_id"]
        self.role = token.get("role")
        self.is_phone_verified = token.get("is_phone_verified")
        self.is_authenticated = True


class ClaimsBasedJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        return ClaimsBasedUser(validated_token)
