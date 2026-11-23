from aeropuerto.forms import AeronaveForm
from aeropuerto.models import Aeronave
from .crud import entity_create, entity_delete, entity_detail, entity_list, entity_update


def aeronave_list(request):
    return entity_list(request, Aeronave, "aeropuerto/aeronaves/aeronave_list.html")


def aeronave_detail(request, pk):
    return entity_detail(request, Aeronave, "aeropuerto/aeronaves/aeronave_detail.html", pk)


def aeronave_create(request):
    return entity_create(
        request,
        Aeronave,
        AeronaveForm,
        "aeropuerto/aeronaves/aeronave_form.html",
        "aeronaves:aeronave_list",
    )


def aeronave_update(request, pk):
    return entity_update(
        request,
        Aeronave,
        AeronaveForm,
        "aeropuerto/aeronaves/aeronave_form.html",
        "aeronaves:aeronave_detail",
        pk,
    )


def aeronave_delete(request, pk):
    return entity_delete(
        request,
        Aeronave,
        "aeropuerto/aeronaves/aeronave_confirm_delete.html",
        "aeronaves:aeronave_list",
        pk,
    )
