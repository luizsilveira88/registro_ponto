from rest_framework import serializers
from ..models.colaborador import Colaborador


class ColaboradorBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colaborador
        fields = [
            "id",
            "nome",
            "cnpj",
        ]


class ColaboradorSaveSerializer(serializers.ModelSerializer):
    emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Colaborador
        fields = [
            "cnpj",
            "nome",
            "cidade",
            "status",
            "organizacao",
            "emails",
        ]


class ColaboradorListSerializer(ColaboradorBaseSerializer):
    get_cidade_display = serializers.CharField(source="cidade.nome")

    class Meta(ColaboradorBaseSerializer.Meta):
        fields = ColaboradorBaseSerializer.Meta.fields + [
            "cidade",
            "get_status_display",
            "get_cidade_display",
        ]


class ColaboradorDetailSerializer(ColaboradorListSerializer):
    organizacao = serializers.CharField(source="organizacao.nome")

    class Meta(ColaboradorListSerializer.Meta):
        fields = ColaboradorListSerializer.Meta.fields + [
            "organizacao",
        ]
