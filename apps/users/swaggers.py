from drf_yasg import openapi

naver_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "code": openapi.Schema(type=openapi.TYPE_STRING),
        "state": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=["code", "state"],
)

naver_responses = {
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
}

check_nickname_request_query = openapi.Parameter(
    "nickname",
    openapi.IN_QUERY,
    description="accesstoken은 필수입니다.",
    type=openapi.TYPE_STRING,
    required=True,
)

check_nickname_responses = {
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
}


dev_auth_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "nickname": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=[
        "nickname",
    ],
)
