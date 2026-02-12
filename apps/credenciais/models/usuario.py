from django.db import models
from django.conf import settings


class Usuario(models.Model):
    nome = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    cpf = models.CharField(
        max_length=11,
        unique=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usuario",
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome
