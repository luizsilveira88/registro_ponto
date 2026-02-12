from django.forms.widgets import TextInput
from django.urls import reverse_lazy


class CNPJInput(TextInput):
    template_name = "core/widgets/cnpj_input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = reverse_lazy("usuario_api:usuario-fetch-cnpj")

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["cnpj_api_url"] = self.base_url
        return context
