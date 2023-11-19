import logging
from datetime import datetime

from django.http import JsonResponse
from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from apps.users.jwt import check_jwt_expired_date, decode_jwt
from apps.users.models import User

logger = logging.getLogger(__name__)


class JsonWebTokenMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if (
                request.path != "/api/users/auth/naver"
                and request.path != "/api/users/auth/dev"
                and request.path != "/api/users/check-nickname"
                and request.path != "/api/users/test"
                and "admin" not in request.path
                and "swagger" not in request.path
                and "redoc" not in request.path
            ):
                access_token = request.headers.get("Authorization", None)
                logger.info(access_token)
                if not access_token:
                    raise PermissionDenied()

                auth_type, token = access_token.split(" ")
                if auth_type == "Bearer":
                    payload = decode_jwt(token)
                    if not payload:
                        raise PermissionDenied("permission denied")

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    token_expired = payload.get("expired")

                    if check_jwt_expired_date(now, token_expired):
                        raise ExpiredSignatureError()

                    user_id = payload.get("user_id", None)
                    if not user_id:
                        raise PermissionDenied()

                else:
                    raise PermissionDenied()

            response = self.get_response(request)
            return response

        except (PermissionDenied, User.DoesNotExist):
            return JsonResponse(
                {"error": "Authorization Error"}, status=status.HTTP_401_UNAUTHORIZED
            )

        except ExpiredSignatureError:
            return JsonResponse(
                {"error": "Expired token. Please log in again."},
                status=status.HTTP_403_FORBIDDEN,
            )
