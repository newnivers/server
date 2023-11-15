from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.swaggers import auth_parameter
from apps.core.views import BaseViewSet
from apps.users.jwt import generate_access_jwt
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.users.swaggers import (
    check_nickname_request_query,
    check_nickname_responses,
    dev_auth_request_body,
    naver_request_body,
    naver_responses,
)
from apps.users.utils import (
    check_duplicate_nickname,
    get_naver_access_token,
    get_naver_user_info,
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="My page 조회 API",
        manual_parameters=[auth_parameter],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.get_response(
            "유저 정보 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="User 수정 API",
        manual_parameters=[auth_parameter],
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return self.get_response(
            "유저 정보 수정에 성공하였습니다.", serializer.data, status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="계정 삭제 API",
        manual_parameters=[auth_parameter],
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
        request_body=naver_request_body,
        responses=naver_responses,
    )
    @action(methods=["POST"], detail=False, url_path="auth/naver")
    def naver(self, request):
        data = request.data.copy()

        code = data.get("code", None)
        state = data.get("state", None)

        if not (code or state):
            return self.get_response(
                "code와 state값은 필수입니다.", {}, status.HTTP_400_BAD_REQUEST
            )

        naver_access_token = get_naver_access_token(code, state)

        if not naver_access_token:
            return self.get_response("유효한 code가 아닙니다.", {}, status.HTTP_400_BAD_REQUEST)

        naver_user_info = get_naver_user_info(naver_access_token)
        if not naver_user_info:
            return self.get_response(
                "네이버 유저정보를 가져오는데 실패했습니다.", {}, status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(social_id=naver_user_info["id"])
            _message = "로그인에 성공했습니다."
            _status = status.HTTP_200_OK

        except User.DoesNotExist:
            user = User.objects.create(
                nickname=naver_user_info["nickname"],
                social_id=naver_user_info["id"],
            )
            _message = "회원가입에 성공하였습니다."
            _status = status.HTTP_201_CREATED
        return self.get_response(
            _message,
            {
                "token": generate_access_jwt(user.id),
                "user_id": user.id,
                "nickname": user.nickname,
            },
            _status,
        )

    @swagger_auto_schema(
        operation_summary="nickname 중복체크 API",
        manual_parameters=[check_nickname_request_query],
        responses=check_nickname_responses,
    )
    @action(methods=["GET"], detail=False, url_path="check-nickname")
    def check_nickname(self, request):
        nickname = request.query_params.get("nickname", None)
        if nickname and not check_duplicate_nickname(nickname):
            return self.get_response(
                "사용 가능한 닉네임 입니다.", {"is_duplicated": True}, status.HTTP_200_OK
            )
        return self.get_response(
            "사용 불가능한 닉네임 입니다.", {"is_duplicated": False}, status.HTTP_409_CONFLICT
        )


class DevAuthView(BaseViewSet):
    @swagger_auto_schema(
        operation_summary="개발용 토큰 발급 API",
        operation_description="개발 환경에서만 유효한 api입니다. 운영환경에서는 활성화 되어있지 않습니다.",
        request_body=dev_auth_request_body,
        responses=naver_responses,
    )
    @action(methods=["POST"], detail=False, url_path="auth/dev")
    def dev(self, request):
        data = request.data.copy()

        nickname = data.get("nickname", None)

        if not nickname:
            return self.get_response(
                "nickname값은 필수입니다.", {}, status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(nickname=nickname)
            _message = "로그인에 성공했습니다."
            _status = status.HTTP_200_OK

        except User.DoesNotExist:
            user = User.objects.create(
                nickname=nickname,
                social_id=nickname,
            )
            _message = "회원가입에 성공하였습니다."
            _status = status.HTTP_201_CREATED
        return self.get_response(
            _message,
            {
                "token": generate_access_jwt(user.id),
                "user_id": user.id,
                "nickname": user.nickname,
            },
            _status,
        )
