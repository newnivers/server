from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status

from apps.arts.models import Art
from apps.arts.serializers import ArtSerializer
from apps.core.swaggers import auth_parameter
from apps.core.views import BaseViewSet


class ArtViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    BaseViewSet,
):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer

    @swagger_auto_schema(
        operation_summary="작품 리스트 조회 API",
        manual_parameters=[auth_parameter],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_response(
            "작품 리스트 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="작품 상세 조회 API",
        manual_parameters=[auth_parameter],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.get_response(
            "작품 상세 정보 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="작품 생성 API",
        manual_parameters=[auth_parameter],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.get_response("작품 생성에 성공했습니다.", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="작품 수정 API",
        manual_parameters=[auth_parameter],
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
        return self.get_response("작품 수정에 성공했습니다.", serializer.data, status.HTTP_200_OK)
