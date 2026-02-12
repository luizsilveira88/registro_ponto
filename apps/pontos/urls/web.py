from django.urls import path
from ..web import ponto_web

app_name = "ponto_web"

urlpatterns = [
    # coleção (lista)
    path(
        "pontos/",
        ponto_web.list,
        name="ponto-list",
    ),
    # instância (detalhe)
    path(
        "pontos/<int:ponto_id>/",
        ponto_web.detail,
        name="ponto-detail",
    ),
]
