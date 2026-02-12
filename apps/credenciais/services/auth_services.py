from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from ..models.usuario import Usuario
from ..serializers.usuario_serializers import UsuarioSessionSerializer


def login_user(request, username, password):
    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if not user:
        raise PermissionError("Usuário ou senha inválidos")

    login(request, user)

    try:
        usuario = Usuario.objects.get(user__id=user.id)
    except Usuario.DoesNotExist:
        logout(request)
        raise PermissionError("Usuário sem permissão de acesso")

    serializer = UsuarioSessionSerializer(usuario)

    request.session["usuario"] = serializer.data
    request.session["config"] = {
        "sidebar_minimize": 0,
    }


def logout_user(request):
    logout(request)
    request.session.flush()
