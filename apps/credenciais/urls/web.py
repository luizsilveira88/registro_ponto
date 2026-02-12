from django.urls import path

from apps.credenciais.web import usuario_web, auth_web

app_name = "auth_web"

urlpatterns = [
    # Usuarios (WEB)
    path(
        "usuarios/",
        usuario_web.list,
        name="usuarios-list",
    ),
    path(
        "usuarios/<int:usuario_id>/",
        usuario_web.detail,
        name="usuarios-detail",
    ),
    # Auth (WEB)
    path(
        "login/",
        auth_web.login_view,
        name="login",
    ),
    path(
        "logout/",
        auth_web.logout_view,
        name="logout",
    ),
]
