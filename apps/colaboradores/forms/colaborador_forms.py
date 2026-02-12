from django import forms
from ..models.colaborador import Colaborador
from core.widgets import CNPJInput


class ColaboradorForm(forms.ModelForm):

    class Meta:
        model = Colaborador
        fields = [
            "nome",
            "email",
        ]
