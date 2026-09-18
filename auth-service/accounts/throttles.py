from rest_framework.throttling import ScopedRateThrottle


class PhoneNumberRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": phone_number,
        }
