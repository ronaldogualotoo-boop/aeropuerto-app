from aeropuerto.forms import VueloForm
from aeropuerto.models import Vuelo
from .crud import entity_create, entity_delete, entity_detail, entity_list, entity_update


def vuelo_list(request):
    return entity_list(request, Vuelo, "aeropuerto/vuelos/vuelo_list.html")


def vuelo_detail(request, pk):
    return entity_detail(request, Vuelo, "aeropuerto/vuelos/vuelo_detail.html", pk)


def vuelo_create(request):
    return entity_create(
        request,
        Vuelo,
        VueloForm,
        "aeropuerto/vuelos/vuelo_form.html",
        "vuelos:vuelo_list",
    )


def vuelo_update(request, pk):
    return entity_update(
        request,
        Vuelo,
        VueloForm,
        "aeropuerto/vuelos/vuelo_form.html",
        "vuelos:vuelo_detail",
        pk,
    )


def vuelo_delete(request, pk):
    return entity_delete(
        request,
        Vuelo,
        "aeropuerto/vuelos/vuelo_confirm_delete.html",
        "vuelos:vuelo_list",
        pk,
    )
