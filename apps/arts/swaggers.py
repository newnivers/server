from drf_yasg import openapi

from apps.arts import CategoryChoices, StatusChoices

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


art_schedule_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "start_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "end_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "seat_count": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=["start_at", "end_at", "seat_count"],
)

art_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "place": openapi.Schema(type=openapi.TYPE_INTEGER),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
        "genre": openapi.Schema(type=openapi.TYPE_STRING),
        "status": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=StatusChoices.values,
            default=StatusChoices.PENDING,
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_STRING, enum=CategoryChoices.values
        ),
        "running_time": openapi.Schema(type=openapi.TYPE_INTEGER),
        "age_limit": openapi.Schema(type=openapi.TYPE_INTEGER, default=0),
        "inter_mission": openapi.Schema(type=openapi.TYPE_INTEGER, default=0),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "caution_description": openapi.Schema(type=openapi.TYPE_STRING),
        "cs_phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "is_free": openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
        "reserved_seat": openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
        "purchase_limit_count": openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER),
        # "schedules": openapi.Schema(
        #     type=openapi.TYPE_ARRAY,
        #     items=art_schedule_schema,
        #     minItems=1,
        # ),
        "ticket_open_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "ticket_close_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
    },
    required=[
        "place",
        "title",
        "image",
        "genre",
        "category",
        "running_time",
        "description",
        "caution_description",
        "cs_phone_number",
        "price",
        "schedules",
        "ticket_open_at",
        "ticket_close_at",
    ],
)

art_schedule_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "startAt": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "endAt": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "seatCount": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=["id", "startAt", "endAt", "seatCount"],
)

art_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "user": openapi.Schema(type=openapi.TYPE_INTEGER),
        "place": openapi.Schema(type=openapi.TYPE_STRING),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "image": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
        "genre": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(
            type=openapi.TYPE_STRING, enum=CategoryChoices.values
        ),
        "status": openapi.Schema(type=openapi.TYPE_STRING, enum=StatusChoices.values),
        "runningTime": openapi.Schema(type=openapi.TYPE_INTEGER),
        "ageLimit": openapi.Schema(type=openapi.TYPE_INTEGER),
        "interMission": openapi.Schema(type=openapi.TYPE_INTEGER),
        "description": openapi.Schema(type=openapi.TYPE_STRING),
        "cautionDescription": openapi.Schema(type=openapi.TYPE_STRING),
        "csPhoneNumber": openapi.Schema(type=openapi.TYPE_STRING),
        "reservedSeat": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "startDate": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "endDate": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "isFree": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "purchaseLimitCount": openapi.Schema(type=openapi.TYPE_INTEGER),
        "price": openapi.Schema(type=openapi.TYPE_STRING),
        "ticket_open_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "ticket_close_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
        ),
        "schedules": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=art_schedule_response_schema,
            minItems=1,
        ),
    },
)

section_parameter = openapi.Parameter(
    name="section",
    in_=openapi.IN_QUERY,
    description="Section for filtering.",
    required=False,
    type=openapi.TYPE_STRING,
)
