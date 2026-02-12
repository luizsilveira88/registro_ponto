from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            "apps.colaboradores.urls.api",
            namespace="usuario_api",
        ),
    ),
    path(
        "",
        include(
            "apps.credenciais.urls.api",
            namespace="auth_api",
        ),
    ),
]
