from aeropuerto.forms import AerolineaForm
from aeropuerto.models import Aerolinea
from .crud import entity_create, entity_delete, entity_detail, entity_list, entity_update


def aerolinea_list(request):
    return entity_list(request, Aerolinea, "aeropuerto/aerolineas/aerolinea_list.html")


def aerolinea_detail(request, pk):
    return entity_detail(request, Aerolinea, "aeropuerto/aerolineas/aerolinea_detail.html", pk)


def aerolinea_create(request):
    return entity_create(
        request,
        Aerolinea,
        AerolineaForm,
        "aeropuerto/aerolineas/aerolinea_form.html",
        "aerolineas:aerolinea_list",
    )


def aerolinea_update(request, pk):
    return entity_update(
        request,
        Aerolinea,
        AerolineaForm,
        "aeropuerto/aerolineas/aerolinea_form.html",
        "aerolineas:aerolinea_detail",
        pk,
    )


def aerolinea_delete(request, pk):
    return entity_delete(
        request,
        Aerolinea,
        "aeropuerto/aerolineas/aerolinea_confirm_delete.html",
        "aerolineas:aerolinea_list",
        pk,
    )
