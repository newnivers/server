from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(
    GenericViewSet,
):
    def get_response(self, msg: str, results: dict, status: int):
        return Response({"message": msg, "data": results}, status=status)
