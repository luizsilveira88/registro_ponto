from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            "apps.colaboradores.urls.web",
            namespace="usuario_web",
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
]
