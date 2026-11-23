from django import forms

from aeropuerto.models import Vuelo


class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = [
            "codigo",
            "aerolinea",
            "aeronave",
            "origen",
            "destino",
            "salida",
            "llegada",
            "estado",
        ]
        widgets = {
            "salida": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "llegada": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        origen = cleaned_data.get("origen")
        destino = cleaned_data.get("destino")
        salida = cleaned_data.get("salida")
        llegada = cleaned_data.get("llegada")
        if origen and destino and origen == destino:
            self.add_error("destino", "El origen y el destino deben ser distintos.")
        if salida and llegada and llegada <= salida:
            self.add_error("llegada", "La llegada debe ser posterior a la salida.")
        return cleaned_data
