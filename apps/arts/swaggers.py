from drf_yasg import openapi

categories_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "categories": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
            ),
        },
    ),
}
