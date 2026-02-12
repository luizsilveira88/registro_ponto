# Django
from django.template.response import TemplateResponse

# DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def public_home(request):
    return TemplateResponse(request, "public/public_home.html")


def orcamento(request):
    context = {}
    return TemplateResponse(request, "public/public_orcamento.html", context)


@api_view(["POST"])
def orcamento_save(request):
    pass
    # return _save_prospeccao_data(request)
