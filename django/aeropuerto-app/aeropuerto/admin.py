from django.contrib import admin

from aeropuerto.models import Aeronave, Aerolinea, Aeropuerto, Vuelo


@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ("codigo_iata", "nombre", "ciudad", "pais", "creado_por")
    list_filter = ("pais", "ciudad")
    search_fields = ("codigo_iata", "nombre", "ciudad")


@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "pais_origen", "creado_por")
    list_filter = ("pais_origen",)
    search_fields = ("codigo", "nombre", "pais_origen")


@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ("matricula", "fabricante", "modelo", "capacidad", "aerolinea")
    list_filter = ("fabricante", "aerolinea")
    search_fields = ("matricula", "fabricante", "modelo")


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ("codigo", "aerolinea", "origen", "destino", "salida", "estado")
    list_filter = ("estado", "aerolinea", "salida")
    search_fields = ("codigo", "origen__nombre", "destino__nombre", "aerolinea__nombre")
