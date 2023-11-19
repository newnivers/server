from drf_yasg import openapi

auth_parameter = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="accesstoken은 필수입니다.",
    type=openapi.TYPE_STRING,
    required=True,
)

start_date_parameter = openapi.Parameter(
    name="start_date",
    in_=openapi.IN_QUERY,
    description="Start date for filtering.",
    required=False,
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)
end_date_parameter = openapi.Parameter(
    name="end_date",
    in_=openapi.IN_QUERY,
    description="End date for filtering.",
    required=False,
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)
