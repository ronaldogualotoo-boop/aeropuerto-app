from aeropuerto.forms import AeropuertoForm
from aeropuerto.models import Aeropuerto
from .crud import entity_create, entity_delete, entity_detail, entity_list, entity_update


def aeropuerto_list(request):
    return entity_list(request, Aeropuerto, "aeropuerto/aeropuertos/aeropuerto_list.html")


def aeropuerto_detail(request, pk):
    return entity_detail(request, Aeropuerto, "aeropuerto/aeropuertos/aeropuerto_detail.html", pk)


def aeropuerto_create(request):
    return entity_create(
        request,
        Aeropuerto,
        AeropuertoForm,
        "aeropuerto/aeropuertos/aeropuerto_form.html",
        "aeropuertos:aeropuerto_list",
    )


def aeropuerto_update(request, pk):
    return entity_update(
        request,
        Aeropuerto,
        AeropuertoForm,
        "aeropuerto/aeropuertos/aeropuerto_form.html",
        "aeropuertos:aeropuerto_detail",
        pk,
    )


def aeropuerto_delete(request, pk):
    return entity_delete(
        request,
        Aeropuerto,
        "aeropuerto/aeropuertos/aeropuerto_confirm_delete.html",
        "aeropuertos:aeropuerto_list",
        pk,
    )
