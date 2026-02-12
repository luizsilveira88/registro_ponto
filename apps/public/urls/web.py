from django.urls import path
from ..web import public_web

app_name = "public"

urlpatterns = [
    path(
        "orcamento/",
        public_web.orcamento,
        name="orcamento",
    ),
    path(
        "orcamento/save/",
        public_web.orcamento_save,
        name="orcamento_save",
    ),
]
