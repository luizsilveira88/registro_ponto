# Django
from django.contrib import admin

# Models
from .models.colaborador import Colaborador
from .models.biometria import Biometria

# Registrar modelos
admin.site.register(Colaborador)
admin.site.register(Biometria)
