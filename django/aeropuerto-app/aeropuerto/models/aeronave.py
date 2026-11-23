from django.conf import settings
from django.db import models
from django.urls import reverse


class Aeronave(models.Model):
    matricula = models.CharField(max_length=12, unique=True)
    fabricante = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    capacidad = models.PositiveSmallIntegerField()
    aerolinea = models.ForeignKey(
        "Aerolinea",
        on_delete=models.PROTECT,
        related_name="aeronaves",
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="aeronaves_creadas",
    )

    class Meta:
        ordering = ["matricula"]
        verbose_name = "aeronave"
        verbose_name_plural = "aeronaves"

    def __str__(self):
        return f"{self.matricula} — {self.fabricante} {self.modelo}"

    def get_absolute_url(self):
        return reverse("aeronaves:aeronave_detail", kwargs={"pk": self.pk})
