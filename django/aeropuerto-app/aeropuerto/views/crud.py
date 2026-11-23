from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed


def _has_management_access(user, obj, action):
    permission = f"{obj._meta.app_label}.{action}_{obj._meta.model_name}"
    if not user.has_perm(permission):
        return False
    return (
        user.is_superuser
        or user.groups.filter(name="administradores").exists()
        or obj.creado_por_id == user.pk
    )


def entity_list(request, model, template):
    return render(request, template, {"object_list": model.objects.all()})


def entity_detail(request, model, template, pk):
    obj = get_object_or_404(model, pk=pk)
    return render(request, template, {"object": obj})


@login_required
def entity_create(request, model, form_class, template, route_name):
    permission = f"{model._meta.app_label}.add_{model._meta.model_name}"
    if not request.user.has_perm(permission):
        return HttpResponseForbidden("No tienes permiso para crear este registro.")
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creado_por = request.user
            obj.save()
            form.save_m2m()
            messages.success(request, f"{model._meta.verbose_name.title()} creado correctamente.")
            return redirect(route_name, pk=obj.pk) if route_name.endswith("_detail") else redirect(route_name)
    else:
        form = form_class()
    return render(request, template, {"form": form, "object": None})


@login_required
def entity_update(request, model, form_class, template, route_name, pk):
    obj = get_object_or_404(model, pk=pk)
    if not _has_management_access(request.user, obj, "change"):
        return HttpResponseForbidden("No tienes permiso para editar este registro.")
    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model._meta.verbose_name.title()} actualizado correctamente.")
            return redirect(route_name, pk=obj.pk)
    else:
        form = form_class(instance=obj)
    return render(request, template, {"form": form, "object": obj})


@login_required
def entity_delete(request, model, template, route_name, pk):
    obj = get_object_or_404(model, pk=pk)
    if not _has_management_access(request.user, obj, "delete"):
        return HttpResponseForbidden("No tienes permiso para eliminar este registro.")
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{model._meta.verbose_name.title()} eliminado correctamente.")
        return redirect(route_name)
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])
    return render(request, template, {"object": obj})
