from django.db import models


class Colaborador(models.Model):
    class Status(models.IntegerChoices):
        ATIVO = 1
        INATIVO = 2

    nome = models.CharField(max_length=255)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ATIVO,
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.nome
