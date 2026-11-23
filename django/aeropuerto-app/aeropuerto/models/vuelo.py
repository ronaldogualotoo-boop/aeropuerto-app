from django.conf import settings
from django.db import models
from django.urls import reverse


class Vuelo(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADO = "programado", "Programado"
        ABORDANDO = "abordando", "Abordando"
        EN_VUELO = "en_vuelo", "En vuelo"
        COMPLETADO = "completado", "Completado"
        CANCELADO = "cancelado", "Cancelado"

    codigo = models.CharField(max_length=8, unique=True)
    aerolinea = models.ForeignKey(
        "Aerolinea",
        on_delete=models.PROTECT,
        related_name="vuelos",
    )
    aeronave = models.ForeignKey(
        "Aeronave",
        on_delete=models.PROTECT,
        related_name="vuelos",
    )
    origen = models.ForeignKey(
        "Aeropuerto",
        on_delete=models.PROTECT,
        related_name="vuelos_salida",
    )
    destino = models.ForeignKey(
        "Aeropuerto",
        on_delete=models.PROTECT,
        related_name="vuelos_llegada",
    )
    salida = models.DateTimeField()
    llegada = models.DateTimeField()
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PROGRAMADO,
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vuelos_creados",
    )

    class Meta:
        ordering = ["salida"]
        verbose_name = "vuelo"
        verbose_name_plural = "vuelos"

    def __str__(self):
        return f"{self.codigo}: {self.origen.codigo_iata} → {self.destino.codigo_iata}"

    def get_absolute_url(self):
        return reverse("vuelos:vuelo_detail", kwargs={"pk": self.pk})
