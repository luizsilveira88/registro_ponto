from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            "apps.colaboradores.urls.web",
            namespace="colaborador_web",
        ),
    ),
    path(
        "",
        include(
            "apps.public.urls.web",
            namespace="public_web",
        ),
    ),
    path(
        "",
        include(
            "apps.credenciais.urls.web",
            namespace="auth_web",
        ),
    ),
    path(
        "",
        include(
            "apps.pontos.urls.web",
            namespace="ponto_web",
        ),
    ),
]
