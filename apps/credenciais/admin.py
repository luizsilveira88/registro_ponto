# Django
from django.contrib import admin

# Models
from .models.usuario import Usuario

# Registrar modelos
admin.site.register(Usuario)
