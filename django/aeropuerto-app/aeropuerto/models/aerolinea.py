from django.conf import settings
from django.db import models
from django.urls import reverse


class Aerolinea(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=120)
    pais_origen = models.CharField(max_length=100)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="aerolineas_creadas",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "aerolínea"
        verbose_name_plural = "aerolíneas"

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"

    def get_absolute_url(self):
        return reverse("aerolineas:aerolinea_detail", kwargs={"pk": self.pk})
