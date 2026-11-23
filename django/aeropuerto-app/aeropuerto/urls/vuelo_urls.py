from django.urls import path

from aeropuerto.views import vuelo_create, vuelo_delete, vuelo_detail, vuelo_list, vuelo_update

app_name = "vuelos"

urlpatterns = [
    path("", vuelo_list, name="vuelo_list"),
    path("nuevo/", vuelo_create, name="vuelo_create"),
    path("<int:pk>/", vuelo_detail, name="vuelo_detail"),
    path("<int:pk>/editar/", vuelo_update, name="vuelo_update"),
    path("<int:pk>/eliminar/", vuelo_delete, name="vuelo_delete"),
]
