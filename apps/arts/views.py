from io import BytesIO

import qrcode
from django.core.cache import cache
from django.core.files import File
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.arts import CategoryChoices, StatusChoices
from apps.arts.models import Art, Ticket, Comment, ArtSchedule
from apps.arts.serializers import ArtSerializer, TicketSerializer, CommentSerializer, ArtScheduleSerializer
from apps.arts.swaggers import (
    art_request_body,
    art_response_schema,
    categories_responses, section_parameter, reserve_schema,
)
from apps.arts.utils import check_valid_ip_for_hit_count
from apps.core.swaggers import auth_parameter, end_date_parameter, start_date_parameter
from apps.core.utils import get_client_ip
from apps.core.views import BaseViewSet


class ArtViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    BaseViewSet,
):
    serializer_class = ArtSerializer

    def get_queryset(self):
        q = Q()

        if self.action == "list":
            start_date = self.request.query_params.get("start_date", None)
            end_date = self.request.query_params.get("end_date", None)

            if start_date:
                q &= Q(created_at__gte=start_date)
            if end_date:
                q &= Q(created_at__lte=end_date)

        q &= Q(status=StatusChoices.APPROVED)
        return Art.objects.filter(q)

    @swagger_auto_schema(
        operation_summary="작품 리스트 조회 API",
        manual_parameters=[
            start_date_parameter,
            end_date_parameter,
            section_parameter,
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        section = self.request.query_params.get('section', None)


        if not section or section == 'Home':
            hot_ranking = queryset.order_by('-hit_count')[:3]
            ticket_open = queryset.filter(ticket_open_at__gte=timezone.now()).order_by('-ticket_open_at')

            hot_ranking_page = self.paginate_queryset(hot_ranking)
            ticket_open_page = self.paginate_queryset(ticket_open)

            hot_ranking_serializer = self.get_serializer(hot_ranking_page, many=True)
            ticket_open_page_serializer = self.get_serializer(ticket_open_page, many=True)

            results = {
                'hot_ranking': hot_ranking_serializer.data,
                'ticket_open': ticket_open_page_serializer.data,
            }

        return self.get_response("작품 리스트 조회에 성공했습니다.", results, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="작품 상세 조회 API",
        manual_parameters=[],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not check_valid_ip_for_hit_count(request):
            instance.hit_count += 1
            instance.save()
            cache.set(get_client_ip(request), 1, 60 * 60 * 24)
        serializer = self.get_serializer(instance)
        return self.get_response("작품 상세 정보 조회에 성공했습니다.", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="작품 생성 API",
        manual_parameters=[auth_parameter],
        request_body=art_request_body,
        responses={201: art_response_schema},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.get_response("작품 생성에 성공했습니다.", serializer.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="작품 수정 API",
        manual_parameters=[auth_parameter],
        request_body=art_request_body,
        responses={200: art_response_schema},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return self.get_response("작품 수정에 성공했습니다.", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="작품 카테고리 리스트 조회 API",
        manual_parameters=[auth_parameter],
        responses=categories_responses,
    )
    @action(methods=["GET"], detail=False)
    def categories(self, request):
        return self.get_response(
            "작품 카테고리 리스트 조회에 성공했습니다.",
            {"categories": CategoryChoices.values},
            status.HTTP_200_OK,
        )


class ArtScheduleViewSet(
    BaseViewSet,
):
    queryset = ArtSchedule
    serializer_class = ArtScheduleSerializer

    @swagger_auto_schema(
        operation_summary= "티켓 예약 API",
        manual_parameters=[auth_parameter],
        request_body=reserve_schema,
    )
    @action(methods=["POST"], detail=True)
    def reserve_tickets(self, request, pk):
        quantity = request.data.get('quantity', 1)
        tickets = Ticket.objects.filter(art_schedule__id=pk, is_sold_out=False)[:quantity]

        for ticket in tickets:
            ticket.is_sold_out = True
            ticket.user = request.user
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data("https://www.naver.com")
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            ticket.qr_code.save(f"{ticket.id}.png", File(buffer), save=True)
            ticket.save()
        return self.get_response(
            "티켓 예약에 성공했습니다.",
            {},
            status.HTTP_200_OK,
        )


class TicketViewSet(
    mixins.RetrieveModelMixin,
    BaseViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @swagger_auto_schema(
        operation_summary="티켓 상세 조회 API",
        manual_parameters=[auth_parameter],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.get_response(
            "티켓 상세 정보 조회에 성공했습니다.",
            serializer.data,
            status.HTTP_200_OK,
        )

    @swagger_auto_schema(operation_summary="티켓 예매 API", manual_parameters=[auth_parameter], request_body=no_body)
    @action(methods=["POST"], detail=True)
    def reserve(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        ticket.is_sold_out = True
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("https://www.naver.com")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        ticket.qr_code.save(f"{ticket.id}.png", File(buffer), save=True)
        ticket.save()

        return self.get_response(
            "티켓 예매에 성공하였습니다..",
            {},
            status.HTTP_200_OK,
        )


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     BaseViewSet,):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @swagger_auto_schema(
        operation_summary="작품 후기 생성 API",
        manual_parameters=[
            auth_parameter,
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.get_response("후기 생성에 성공했습니다.", serializer.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="작품 후기 수정 API",
        manual_parameters=[
            auth_parameter,
        ],
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.get_response("후기 수정에 성공했습니다.", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="작품 후기 삭제 API",
        manual_parameters=[
            auth_parameter,
        ],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.get_response("후기 삭제에 성공했습니다.", status.HTTP_204_NO_CONTENT)
