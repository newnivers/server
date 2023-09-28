from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.jwt import generate_access_jwt
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.users.utils import (
    check_duplicate_nickname,
    get_naver_access_token,
    get_naver_user_info,
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="My page 조회 API",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="accesstoken은 필수입니다.",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="User 수정 API",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="accesstoken은 필수입니다.",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="계정 삭제 API",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="accesstoken은 필수입니다.",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

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

    @swagger_auto_schema(
        operation_summary="nickname 중복체크 API",
        manual_parameters=[
            openapi.Parameter(
                "nickname",
                openapi.IN_QUERY,
                description="accesstoken은 필수입니다.",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "is_duplicated": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                },
            ),
            409: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "is_duplicated": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                },
            ),
        },
    )
    @action(methods=["GET"], detail=False, url_path="check-nickname")
    def check_nickname(self, request):
        nickname = request.query_params.get("nickname", None)
        if nickname and not check_duplicate_nickname(nickname):
            return Response(
                {
                    "message": "사용가능한 닉네임 입니다.",
                    "results": {"is_duplicated": True},
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "사용불가능한 닉네임 입니다.",
                "results": {"is_duplicated": False},
            },
            status=status.HTTP_409_CONFLICT,
        )
