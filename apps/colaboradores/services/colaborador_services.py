# Django
from django.db import transaction
from django.shortcuts import get_object_or_404

# Models
from apps.colaboradores.models.colaborador import Colaborador


# Serializers
from apps.colaboradores.serializers.colaborador_serializers import (
    ColaboradorSaveSerializer,
)

# Exceptions
from apps.colaboradores.exceptions.colaborador_exceptions import (
    ColaboradorNotFound,
    CNPJServiceError,
)

# Services
from ..services.biometria_services import create_biometria


def list_colaboradors() -> list:
    return Colaborador.objects.all().order_by("nome")


def get_colaborador(pk: int) -> Colaborador:
    try:
        return Colaborador.objects.get(pk=pk)
    except Colaborador.DoesNotExist:
        raise ColaboradorNotFound()


def create_colaborador(data: dict) -> Colaborador:
    serializer = ColaboradorSaveSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def update_colaborador(pk: int, data: dict) -> Colaborador:
    colaborador = get_colaborador(pk)

    serializer = ColaboradorSaveSerializer(
        colaborador,
        data=data,
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return colaborador


def dados_principais(pk: int) -> Colaborador:
    return get_colaborador(pk)


def create_colaborador_with_biometria(data: dict, file) -> Colaborador:
    with transaction.atomic():
        colaborador = create_colaborador(data)
        create_biometria(colaborador, file)

    return colaborador
