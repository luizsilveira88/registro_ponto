from rest_framework import serializers
from ..models.ponto import Ponto


class PontoSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponto
        fields = "__all__"


class PontoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponto
        fields = [
            "id",
            "data",
            "hora",
        ]


class PontoListSerializer(PontoBaseSerializer):
    colaborador = serializers.CharField(source="colaborador.nome")

    class Meta(PontoBaseSerializer.Meta):
        fields = PontoBaseSerializer.Meta.fields + [
            "colaborador",
        ]


class PontoDetailSerializer(PontoListSerializer):
    pass
