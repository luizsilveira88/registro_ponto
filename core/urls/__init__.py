from django.urls import path, include
from ..web.home_web import core_home

app_name = "core"

urlpatterns = [
    path(
        "",
        core_home,
        name="core_home",
    ),
]
