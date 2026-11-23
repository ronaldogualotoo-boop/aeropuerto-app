from django.urls import include, path

urlpatterns = [
    path("", include("aeropuerto.urls.home_urls")),
    path("cuentas/", include("aeropuerto.urls.auth_urls")),
    path("aeropuertos/", include("aeropuerto.urls.aeropuerto_urls")),
    path("aerolineas/", include("aeropuerto.urls.aerolinea_urls")),
    path("aeronaves/", include("aeropuerto.urls.aeronave_urls")),
    path("vuelos/", include("aeropuerto.urls.vuelo_urls")),
]
