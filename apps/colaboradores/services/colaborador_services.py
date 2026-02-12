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


def list_colaboradors() -> list:
    return Colaborador.objects.all().order_by("nome")


def get_colaborador(pk: int) -> Colaborador:
    try:
        return Colaborador.objects.get(pk=pk)
    except Colaborador.DoesNotExist:
        raise ColaboradorNotFound()


def create_colaborador(data: dict, organizacao_id: int) -> Colaborador:
    data = data.copy()
    data["organizacao"] = organizacao_id

    if "emails" in data and isinstance(data["emails"], str):
        data["emails"] = [e.strip() for e in data["emails"].split(",") if e.strip()]

    with transaction.atomic():
        colaborador_serializer = ColaboradorSaveSerializer(data=data)
        colaborador_serializer.is_valid(raise_exception=True)
        colaborador = colaborador_serializer.save()

        config_data = data.copy()
        config_data["colaborador"] = colaborador.id

    return colaborador


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
