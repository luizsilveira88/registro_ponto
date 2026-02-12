# Django
from django.template.response import TemplateResponse

# Core
from core.utils import get_plugins_files

"""
TEMPLATES
"""


def internal_home(request):
    plugins = [
        "apexcharts",
        "flatpickr",
    ]
    context = {
        "js": [
            "usuario/index/js/index.js",
        ],
        "plugins": get_plugins_files(plugins),
    }
    return TemplateResponse(request, "core/home/home.html", context)
