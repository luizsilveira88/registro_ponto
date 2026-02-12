from rest_framework import serializers
from ..models.colaborador import Colaborador


class ColaboradorSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = "__all__"


class ColaboradorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = [
            "id",
            "nome",
        ]


class ColaboradorListSerializer(ColaboradorBaseSerializer):
    class Meta(ColaboradorBaseSerializer.Meta):
        fields = ColaboradorBaseSerializer.Meta.fields + [
            "email",
            "get_status_display",
        ]


class ColaboradorDetailSerializer(ColaboradorListSerializer):
    pass
