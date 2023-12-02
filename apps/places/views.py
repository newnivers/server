from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.swaggers import auth_parameter
from apps.core.views import BaseViewSet
from apps.places.models import Place
from apps.places.serializers import PlaceSerializer


class PlaceViewSet(
    ReadOnlyModelViewSet,
    BaseViewSet,
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @swagger_auto_schema(
        operation_summary="장소 상세 조회 API(현재 사용성 논의 필요)",
        manual_parameters=[auth_parameter],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.get_response("장소 상세 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="장소 리스트 조회 API",
        manual_parameters=[auth_parameter],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_response("장소 리스트 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK)
