# Django
from django.middleware.csrf import get_token
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.decorators import permission_required


# Core
from core.utils import get_plugins_files


# @permission_required("usuario.view_usuario")
def list(request):
    """
    Exibe a página de listagem de usuarios.
    Esse view é responsável por renderizar a página de listagem de usuarios.
    """

    plugin_list = {
        "tom-select",
    }
    context = {
        "js": [
            "usuario/usuario/js/index.js",
        ],
        "plugins": get_plugins_files(plugin_list),
    }
    return TemplateResponse(request, "usuario/usuario/index.html", context)


# @permission_required("usuario.view_usuario")
def detail(request, usuario_id):
    """
    Exibe a página de detalhes de um usuario.
    Esse view é responsável por renderizar a página de detalhes de um usuario.
    """
    context = {
        "js": [
            "usuario/usuario/js/detail.js",
        ],
    }
    return TemplateResponse(request, "usuario/usuario/detail.html", context)
