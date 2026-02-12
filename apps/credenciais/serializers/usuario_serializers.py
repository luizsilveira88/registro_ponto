# DRF
from rest_framework import serializers

# Models
from ..models.usuario import Usuario


class UsuarioBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "nome",
        ]


class UsuarioSessionSerializer(UsuarioBaseSerializer):

    class Meta(UsuarioBaseSerializer.Meta):
        fields = UsuarioBaseSerializer.Meta.fields + [
            "email",
        ]


class UsuarioListSerializer(UsuarioBaseSerializer):

    class Meta(UsuarioBaseSerializer.Meta):
        fields = UsuarioBaseSerializer.Meta.fields + [
            "get_status_display",
        ]


class UsuarioDetailSerializer(UsuarioBaseSerializer):

    class Meta(UsuarioBaseSerializer.Meta):
        fields = UsuarioBaseSerializer.Meta.fields + [
            "get_status_display",
        ]


class UsuarioSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
