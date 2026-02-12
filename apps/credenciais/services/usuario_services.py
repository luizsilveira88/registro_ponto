# Django
from django.db import transaction
from django.contrib.auth.models import Permission

# Models
from apps.credenciais.models.usuario import Usuario

# Serializers
from apps.credenciais.serializers.usuario_serializers import (
    UsuarioSaveSerializer,
    UsuarioListSerializer,
    UsuarioDetailSerializer,
)

# Config
from django.conf import settings


def listar_usuarios(request):
    """
    Retorna a lista de usuários da organização da sessão.
    """
    organizacao_id = request.session["usuario"]["organizacao"]["id"]

    return Usuario.objects.filter(organizacao_id=organizacao_id).order_by("nome")


def obter_usuario(usuario_id):
    """
    Retorna um usuário pelo ID.
    """
    return Usuario.objects.get(id=usuario_id)


@transaction.atomic
def salvar_usuario(request, usuario_id=None):
    """
    Cria ou atualiza um usuário.
    """
    data = request.data.copy()

    organizacao_id = request.session["usuario"]["organizacao"]["id"]
    data["organizacao"] = organizacao_id

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        serializer = UsuarioSaveSerializer(
            usuario,
            data=data,
            partial=True,
        )
    else:
        serializer = UsuarioSaveSerializer(data=data)

    serializer.is_valid(raise_exception=True)
    return serializer.save()


def obter_usuario_por_sessao(request):
    """
    Retorna o usuário logado via sessão.
    """
    usuario_id = request.session["usuario"]["id"]
    return Usuario.objects.get(id=usuario_id)


def obter_permissoes(usuario_id):
    """
    Retorna as permissões de um usuário.
    """
    usuario = Usuario.objects.get(id=usuario_id)

    return list(usuario.user.user_permissions.values_list("codename", flat=True))


@transaction.atomic
def salvar_permissoes(request, usuario_id):
    """
    Atualiza as permissões de um usuário.
    """
    permissoes = request.data.get("permissions", [])

    usuario = Usuario.objects.get(id=usuario_id)

    usuario.user.user_permissions.clear()

    if permissoes:
        permissions = Permission.objects.filter(codename__in=permissoes)
        usuario.user.user_permissions.add(*permissions)
