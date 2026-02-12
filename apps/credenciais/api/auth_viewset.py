# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

# Core
from core.responses import ResponseSuccess, ResponseError

# Services
from ..services import auth_services


class AuthViewSet(ViewSet):
    """
    ViewSet de autenticação
    (session-based)
    """

    @action(
        detail=False,
        methods=["post"],
        url_path="login",
    )
    def login(self, request):
        try:
            username = request.data.get("login")
            password = request.data.get("password")

            if not username or not password:
                return ResponseError(
                    "Login e senha são obrigatórios",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            auth_services.login_user(
                request,
                username,
                password,
            )

            return ResponseSuccess(
                "Login do usuário realizado com sucesso",
            )

        except PermissionError as e:
            return ResponseError(
                str(e),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        except Exception as e:
            return ResponseError(
                "Erro ao autenticar usuário",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=False,
        methods=["post"],
        url_path="logout",
    )
    def logout(self, request):
        try:
            auth_services.logout_user(request)

            return ResponseSuccess(
                "Logout realizado com sucesso",
            )

        except Exception as e:
            return ResponseError(
                "Erro ao realizar logout",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
