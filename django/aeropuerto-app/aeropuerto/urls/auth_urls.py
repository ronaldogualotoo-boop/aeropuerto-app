from django.urls import path

from aeropuerto.views import login_view, logout_view, registro

urlpatterns = [
    path("registrarse/", registro, name="registro"),
    path("entrar/", login_view, name="login"),
    path("salir/", logout_view, name="logout"),
]
