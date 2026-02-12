# Django
from django.contrib import admin

# Models
from .models.colaborador import Colaborador

# Registrar modelos
admin.site.register(Colaborador)
