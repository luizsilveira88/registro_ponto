# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

# Core
from core.responses import ResponseSuccess, ResponseError

# Services
from ..services import ponto_services

# Models
from ..models.ponto import Ponto

# Serializers
from ..serializers.ponto_serializers import (
    PontoSaveSerializer,
    PontoListSerializer,
    PontoDetailSerializer,
)


class PontoViewSet(ViewSet):
    """
    ViewSet de Ponto
    """

    def list(self, request, *args, **kwargs):
        ponto = ponto_services.list_pontos()
        data = PontoListSerializer(ponto, many=True).data
        return ResponseSuccess(
            "Pontos listados com sucesso",
            data,
        )

    def create(self, request, *args, **kwargs):
        ponto = ponto_services.create_ponto(
            request.data,
        )
        data = PontoDetailSerializer(ponto).data
        return ResponseSuccess(
            "Ponto cadastrado com sucesso",
            data,
            status_code=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        ponto = ponto_services.get_ponto(pk)
        data = PontoDetailSerializer(ponto).data
        return ResponseSuccess(
            "Ponto recuperado com sucesso",
            data,
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        ponto = ponto_services.update_ponto(pk, request.data)
        data = PontoDetailSerializer(ponto).data
        return ResponseSuccess(
            "Ponto atualizado com sucesso",
            data,
        )
