from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            "apps.colaboradores.urls.api",
            namespace="colaborador_api",
        ),
    ),
    path(
        "",
        include(
            "apps.credenciais.urls.api",
            namespace="auth_api",
        ),
    ),
    path(
        "",
        include(
            "apps.pontos.urls.api",
            namespace="ponto_api",
        ),
    ),
]
