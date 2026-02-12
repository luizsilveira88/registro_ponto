from rest_framework.views import exception_handler
from rest_framework import status
from core.responses import ResponseError, ResponseSuccess


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return ResponseError(
            "Erro na requisição",
            response.data,
            response.status_code,
        )

    return ResponseError(
        "Erro interno do servidor",
        str(exc),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
