# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

# Core
from core.responses import ResponseSuccess, ResponseError

# Services
from ..services import colaborador_services

# Models
from ..models.colaborador import Colaborador

# Serializers
from ..serializers.colaborador_serializers import (
    ColaboradorSaveSerializer,
    ColaboradorListSerializer,
    ColaboradorDetailSerializer,
)


class ColaboradorViewSet(ViewSet):
    """
    ViewSet de Colaborador
    """

    def list(self, request, *args, **kwargs):
        colaborador = colaborador_services.list_colaboradors()
        data = ColaboradorListSerializer(colaborador, many=True).data
        return ResponseSuccess(
            "Colaboradores listados com sucesso",
            data,
        )

    def create(self, request, *args, **kwargs):
        colaborador = colaborador_services.create_colaborador(
            request.data,
        )
        data = ColaboradorDetailSerializer(colaborador).data
        return ResponseSuccess(
            "Colaborador cadastrado com sucesso",
            data,
            status_code=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        colaborador = colaborador_services.get_colaborador(pk)
        data = ColaboradorDetailSerializer(colaborador).data
        return ResponseSuccess(
            "Colaborador recuperado com sucesso",
            data,
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        colaborador = colaborador_services.update_colaborador(pk, request.data)
        data = ColaboradorDetailSerializer(colaborador).data
        return ResponseSuccess(
            "Colaborador atualizado com sucesso",
            data,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="cnpj",
    )
    def fetch_cnpj(self, request, *args, **kwargs):
        cnpj = request.data.get("cnpj")

        if not cnpj:
            return ResponseError("CNPJ não informado")

        data = colaborador_services.fetch_cnpj_data(cnpj)

        return ResponseSuccess(
            "Dados recuperados com sucesso",
            data,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="dados-principais",
    )
    def dados_principais(self, request, pk=None, *args, **kwargs):
        colaborador = colaborador_services.dados_principais(pk)
        data = ColaboradorDetailSerializer(colaborador).data
        return ResponseSuccess(
            "Dados principais recuperados com sucesso",
            data,
        )
