from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.users.jwt import decode_jwt
from apps.users.models import User


class JsonWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        message = {"message": "INVALID_TOKEN"}
        access_token = request.headers.get("Authorization", None)
        if not access_token:
            return None

        auth_type, token = access_token.split(" ")
        payload = decode_jwt(token)

        user_id = payload.get("user_id", None)
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
            return user, None
        except User.DoesNotExist:
            raise AuthenticationFailed(message)
