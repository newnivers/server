from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(
    GenericViewSet,
):
    @staticmethod
    def get_response(msg: str, results: dict, status: int):
        return Response({"message": msg, "data": results}, status=status)
