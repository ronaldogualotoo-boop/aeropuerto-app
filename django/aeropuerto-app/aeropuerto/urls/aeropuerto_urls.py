from django.urls import path

from aeropuerto.views import (
    aeropuerto_create,
    aeropuerto_delete,
    aeropuerto_detail,
    aeropuerto_list,
    aeropuerto_update,
)

app_name = "aeropuertos"

urlpatterns = [
    path("", aeropuerto_list, name="aeropuerto_list"),
    path("nuevo/", aeropuerto_create, name="aeropuerto_create"),
    path("<int:pk>/", aeropuerto_detail, name="aeropuerto_detail"),
    path("<int:pk>/editar/", aeropuerto_update, name="aeropuerto_update"),
    path("<int:pk>/eliminar/", aeropuerto_delete, name="aeropuerto_delete"),
]
