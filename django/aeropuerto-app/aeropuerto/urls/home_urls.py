from django.urls import path

from aeropuerto.views import home

urlpatterns = [path("inicio/", home, name="home")]
