from drf_yasg import openapi

auth_parameter = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="accesstoken은 필수입니다.",
    type=openapi.TYPE_STRING,
    required=True,
)
