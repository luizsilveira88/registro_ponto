from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.credenciais.api.usuario_viewset import UsuarioViewSet
from apps.credenciais.api.auth_viewset import AuthViewSet

app_name = "auth_api"

router = DefaultRouter()
router.register(
    r"usuarios",
    UsuarioViewSet,
    basename="usuario",
)
router.register(
    r"auth",
    AuthViewSet,
    basename="auth",
)

urlpatterns = [
    path("", include(router.urls)),
]
