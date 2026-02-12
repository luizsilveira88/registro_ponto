from django.db import models


class Biometria(models.Model):
    class Posicao(models.IntegerChoices):
        INATIVO = 0, "Inativo"
        ATIVO = 1, "Ativo"

    colaborador = models.ForeignKey(
        "colaboradores.Colaborador",
        on_delete=models.CASCADE,
        related_name="biometrias",
    )
    encoding = models.BinaryField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    posicao = models.IntegerField(
        choices=Posicao.choices,
        default=Posicao.ATIVO,
    )

    class Meta:
        verbose_name = "Biometria"
        verbose_name_plural = "Biometrias"

    def __str__(self):
        return f"Colaborador {self.colaborador.nome} - Biometria {self.id}"
