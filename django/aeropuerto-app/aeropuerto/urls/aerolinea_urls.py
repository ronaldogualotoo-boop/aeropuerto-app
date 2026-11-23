from django.urls import path

from aeropuerto.views import (
    aerolinea_create,
    aerolinea_delete,
    aerolinea_detail,
    aerolinea_list,
    aerolinea_update,
)

app_name = "aerolineas"

urlpatterns = [
    path("", aerolinea_list, name="aerolinea_list"),
    path("nuevo/", aerolinea_create, name="aerolinea_create"),
    path("<int:pk>/", aerolinea_detail, name="aerolinea_detail"),
    path("<int:pk>/editar/", aerolinea_update, name="aerolinea_update"),
    path("<int:pk>/eliminar/", aerolinea_delete, name="aerolinea_delete"),
]
