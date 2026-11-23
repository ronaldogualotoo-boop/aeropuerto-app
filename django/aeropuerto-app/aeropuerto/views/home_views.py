from django.shortcuts import render

from aeropuerto.models import Aeronave, Aerolinea, Aeropuerto, Vuelo


def home(request):
    context = {
        "aeropuertos_count": Aeropuerto.objects.count(),
        "aerolineas_count": Aerolinea.objects.count(),
        "aeronaves_count": Aeronave.objects.count(),
        "vuelos_count": Vuelo.objects.count(),
    }
    return render(request, "aeropuerto/home.html", context)
