from django.contrib import admin
from django.urls import path, include
from apps.public.web.public_web import public_home
from core.web.home_web import internal_home

urlpatterns = [
    path("", public_home, name="public_home"),
    path("home/", internal_home, name="internal_home"),
    path("admin/", admin.site.urls),
    # API
    path(
        "api/",
        include("apps.api_urls"),
    ),
    # WEB
    path(
        "",
        include("apps.web_urls"),
    ),
]
