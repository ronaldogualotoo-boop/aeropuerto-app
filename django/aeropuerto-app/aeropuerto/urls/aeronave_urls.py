from django.urls import path

from aeropuerto.views import (
    aeronave_create,
    aeronave_delete,
    aeronave_detail,
    aeronave_list,
    aeronave_update,
)

app_name = "aeronaves"

urlpatterns = [
    path("", aeronave_list, name="aeronave_list"),
    path("nuevo/", aeronave_create, name="aeronave_create"),
    path("<int:pk>/", aeronave_detail, name="aeronave_detail"),
    path("<int:pk>/editar/", aeronave_update, name="aeronave_update"),
    path("<int:pk>/eliminar/", aeronave_delete, name="aeronave_delete"),
]
