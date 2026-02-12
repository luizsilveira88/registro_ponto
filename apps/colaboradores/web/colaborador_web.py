# Django
from django.template.response import TemplateResponse
from django.http import Http404
from django.contrib.auth.decorators import permission_required

# Core
from core.utils import get_plugins_files

# Forms
from ..forms.colaborador_forms import ColaboradorForm

# Models
from ..models.colaborador import Colaborador


@permission_required("colaboradores.view_colaborador")
def list(request):
    """
    Exibe a página de listagem de colaboradores.
    Esse view é responsável por renderizar a página de listagem de colaboradores.
    """

    plugin_list = {
        "choices.js",
        "tabulator",
        "picojs",
    }
    context = {
        "js": [
            "core/js/wizards.min.js",
            "colaboradores/js/colaborador_list.js",
        ],
        "forms": {
            "colaborador": ColaboradorForm(),
        },
        "plugins": get_plugins_files(plugin_list),
    }
    return TemplateResponse(request, "colaboradores/colaborador_list.html", context)


@permission_required("colaboradores.view_colaborador")
def detail(request, colaborador_id):
    """
    Exibe a página de detalhes de um colaborador.
    Esse view é responsável por renderizar a página de detalhes de um colaborador.
    """

    try:
        colaborador = Colaborador.objects.get(id=colaborador_id)
    except Colaborador.DoesNotExist:
        raise Http404("Colaborador não encontrado.")

    plugin_list = {}
    context = {
        "js": [
            "core/js/cards.min.js",
            "colaboradores/js/colaborador_detail.js",
        ],
        "py_vars": {
            "colaborador_id": colaborador_id,
        },
        "forms": {
            "colaborador": ColaboradorForm(),
        },
        "plugins": get_plugins_files(plugin_list),
    }
    return TemplateResponse(request, "colaboradores/colaborador_detail.html", context)
