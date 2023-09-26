from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.jwt import generate_access_jwt
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.users.utils import get_naver_access_token, get_naver_user_info


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="네이버 로그인 API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "state": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["code", "state"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "nickname": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "nickname": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            400: "invalid_value",
        },
    )
    @action(methods=["POST"], detail=False, url_path="auth/naver")
    def naver(self, request):
        data = request.data.copy()

        code = data.get("code", None)
        state = data.get("state", None)

        if not (code or state):
            return Response(
                {"message": "missing_value"}, status=status.HTTP_400_BAD_REQUEST
            )

        naver_access_token = get_naver_access_token(code, state)

        if not naver_access_token:
            return Response(
                {"message": "invalid_value"}, status=status.HTTP_400_BAD_REQUEST
            )

        naver_user_info = get_naver_user_info(naver_access_token)
        if not naver_user_info:
            return Response(
                {"message": "invalid_value"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(social_id=naver_user_info["id"])
            _message = "login_success"
            _status = status.HTTP_200_OK

        except User.DoesNotExist:
            user = User.objects.create(
                nickname=naver_user_info["nickname"],
                social_id=naver_user_info["id"],
            )
            _message = "register_success"
            _status = status.HTTP_201_CREATED

        return Response(
            {
                "message": _message,
                "results": {
                    "token": generate_access_jwt(user.id),
                    "user_id": user.id,
                    "nickname": user.nickname,
                },
            },
            status=_status,
        )
