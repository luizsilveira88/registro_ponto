from django.urls import path
from ..web import colaborador_web

app_name = "colaborador_web"

urlpatterns = [
    # coleção (lista)
    path(
        "colaboradores/",
        colaborador_web.list,
        name="colaborador-list",
    ),
    # instância (detalhe)
    path(
        "colaboradores/<int:colaborador_id>/",
        colaborador_web.detail,
        name="colaborador-detail",
    ),
]
