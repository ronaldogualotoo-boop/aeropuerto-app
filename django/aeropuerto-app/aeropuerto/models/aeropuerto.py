from django.conf import settings
from django.db import models
from django.urls import reverse


class Aeropuerto(models.Model):
    codigo_iata = models.CharField("código IATA", max_length=3, unique=True)
    nombre = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    aerolineas = models.ManyToManyField(
        "Aerolinea", related_name="aeropuertos_atendidos", blank=True
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="aeropuertos_creados",
    )

    class Meta:
        ordering = ["ciudad", "nombre"]
        verbose_name = "aeropuerto"
        verbose_name_plural = "aeropuertos"

    def __str__(self):
        return f"{self.codigo_iata} — {self.nombre}"

    def get_absolute_url(self):
        return reverse("aeropuertos:aeropuerto_detail", kwargs={"pk": self.pk})
