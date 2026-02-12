# Django
from django.db import transaction

# Models
from apps.pontos.models.ponto import Ponto


# Serializers
from apps.pontos.serializers.ponto_serializers import (
    PontoSaveSerializer,
)

# Exceptions
from apps.pontos.exceptions.ponto_exceptions import (
    PontoNotFound,
)


def list_pontos() -> list:
    return Ponto.objects.all().order_by("data", "hora")


def get_ponto(pk: int) -> Ponto:
    try:
        return Ponto.objects.get(pk=pk)
    except Ponto.DoesNotExist:
        raise PontoNotFound()


def create_ponto(data: dict) -> Ponto:
    serializer = PontoSaveSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def update_ponto(pk: int, data: dict) -> Ponto:
    ponto = get_ponto(pk)

    serializer = PontoSaveSerializer(
        ponto,
        data=data,
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return ponto
