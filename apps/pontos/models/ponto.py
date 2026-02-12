from django.db import models


class Ponto(models.Model):
    colaborador = models.ForeignKey(
        "colaboradores.Colaborador",
        on_delete=models.CASCADE,
        related_name="pontos",
    )
    data = models.DateField()
    hora = models.TimeField()
    descricao = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "Ponto"
        verbose_name_plural = "Pontos"

    def __str__(self):
        return self.data.strftime("%d/%m/%Y") + " - " + self.hora.strftime("%H:%M:%S")
