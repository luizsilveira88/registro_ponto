# Django
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.conf import settings
from django.urls import reverse


def login_view(request):
    # pass
    if request.user.is_authenticated:
        return redirect("internal_home")

    context = {
        "jsVars": {
            "url": {
                "auth": {
                    "verify": reverse("auth_api:auth-login"),
                }
            }
        }
    }

    return TemplateResponse(request, "credenciais/auth_login.html", context)


def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)
