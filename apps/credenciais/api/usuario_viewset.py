# Django
from django.contrib.auth.decorators import permission_required

# DRF
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Core
from core.responses import ResponseSuccess, ResponseError

# Models
from apps.credenciais.models.usuario import Usuario

# Serializers
from apps.credenciais.serializers.usuario_serializers import (
    UsuarioListSerializer,
    UsuarioDetailSerializer,
    UsuarioSaveSerializer,
    UsuarioSessionSerializer,
)

# Services (opcional agora, obrigatório depois)
from apps.credenciais.services.usuario_services import (
    listar_usuarios,
    obter_usuario,
    salvar_usuario,
    obter_usuario_por_sessao,
    obter_permissoes,
    salvar_permissoes,
)


class UsuarioViewSet(ModelViewSet):
    """
    ViewSet responsável pelo recurso Usuario.

    URLs:
    - GET    /api/usuarios/
    - POST   /api/usuarios/
    - GET    /api/usuarios/{id}/
    - PATCH  /api/usuarios/{id}/

    Custom actions:
    - POST   /api/usuarios/session/
    - GET    /api/usuarios/{id}/permissions/
    - POST   /api/usuarios/{id}/permissions/
    - POST   /api/usuarios/cnpj/
    """

    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]

    # -------------------------
    # Serializers dinâmicos
    # -------------------------
    def get_serializer_class(self):
        if self.action == "list":
            return UsuarioListSerializer

        if self.action == "retrieve":
            return UsuarioDetailSerializer

        if self.action in ("create", "partial_update"):
            return UsuarioSaveSerializer

        if self.action == "session":
            return UsuarioSessionSerializer

        return UsuarioDetailSerializer

    # -------------------------
    # CRUD padrão
    # -------------------------

    def list(self, request):
        try:
            usuarios = listar_usuarios(request)
            serializer = self.get_serializer(usuarios, many=True)
            return ResponseSuccess("Usuários listados com sucesso", serializer.data)
        except Exception as e:
            return ResponseError(
                "Não foi possível listar os usuários",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            usuario = obter_usuario(pk)
            serializer = self.get_serializer(usuario)
            return ResponseSuccess("Usuário recuperado com sucesso", serializer.data)
        except Usuario.DoesNotExist:
            return ResponseError(
                "Usuário não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return ResponseError(
                "Erro ao recuperar usuário",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            usuario = salvar_usuario(request)
            serializer = self.get_serializer(usuario)
            return ResponseSuccess("Usuário criado com sucesso", serializer.data)
        except Exception as e:
            return ResponseError(
                "Erro ao criar usuário",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def partial_update(self, request, pk=None):
        try:
            usuario = salvar_usuario(request, usuario_id=pk)
            serializer = self.get_serializer(usuario)
            return ResponseSuccess("Usuário atualizado com sucesso", serializer.data)
        except Usuario.DoesNotExist:
            return ResponseError(
                "Usuário não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return ResponseError(
                "Erro ao atualizar usuário",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    # -------------------------
    # Custom actions
    # -------------------------

    @action(detail=False, methods=["post"], url_path="session")
    def session(self, request):
        """
        Retorna o usuário com base na sessão ativa
        POST /api/usuarios/session/
        """
        try:
            usuario = obter_usuario_por_sessao(request)
            serializer = UsuarioSessionSerializer(usuario)
            return ResponseSuccess("Usuário recuperado com sucesso", serializer.data)
        except Exception as e:
            return ResponseError(
                "Sessão inválida",
                error=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=True, methods=["get", "post"], url_path="permissions")
    def permissions(self, request, pk=None):
        """
        GET  /api/usuarios/{id}/permissions/
        POST /api/usuarios/{id}/permissions/
        """
        try:
            if request.method == "GET":
                data = obter_permissoes(pk)
                return ResponseSuccess("Permissões recuperadas", data)

            if request.method == "POST":
                salvar_permissoes(request, pk)
                return ResponseSuccess("Permissões salvas com sucesso")

        except Usuario.DoesNotExist:
            return ResponseError(
                "Usuário não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return ResponseError(
                "Erro ao processar permissões",
                error=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
