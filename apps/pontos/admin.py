# Django
from django.contrib import admin

# Models
from .models.ponto import Ponto

# Registrar modelos
admin.site.register(Ponto)
