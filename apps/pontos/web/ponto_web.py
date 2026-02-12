# Django
from django.template.response import TemplateResponse
from django.http import Http404
from django.contrib.auth.decorators import permission_required

# Core
from core.utils import get_plugins_files

# Models
from ..models.ponto import Ponto


@permission_required("pontos.view_ponto")
def list(request):
    """
    Exibe a página de listagem de pontos.
    Esse view é responsável por renderizar a página de listagem de pontos.
    """

    plugin_list = {
        "choices.js",
        "tabulator",
        "picojs",
    }
    context = {
        "js": [
            "core/js/wizards.min.js",
            "pontos/js/ponto_list.js",
        ],
        "plugins": get_plugins_files(plugin_list),
    }
    return TemplateResponse(request, "pontos/ponto_list.html", context)


@permission_required("pontos.view_ponto")
def detail(request, ponto_id):
    """
    Exibe a página de detalhes de um ponto.
    Esse view é responsável por renderizar a página de detalhes de um ponto.
    """

    try:
        ponto = Ponto.objects.get(id=ponto_id)
    except Ponto.DoesNotExist:
        raise Http404("Ponto não encontrado.")

    plugin_list = {}
    context = {
        "js": [
            "core/js/cards.min.js",
            "pontos/js/ponto_detail.js",
        ],
        "py_vars": {
            "ponto_id": ponto_id,
        },
        "plugins": get_plugins_files(plugin_list),
    }
    return TemplateResponse(request, "pontos/ponto_detail.html", context)
