from django import forms

from aeropuerto.models import Aeronave


class AeronaveForm(forms.ModelForm):
    class Meta:
        model = Aeronave
        fields = ["matricula", "fabricante", "modelo", "capacidad", "aerolinea"]
        widgets = {
            "matricula": forms.TextInput(attrs={"placeholder": "HC-ABC"}),
            "capacidad": forms.NumberInput(attrs={"min": 1}),
        }

    def clean_capacidad(self):
        capacidad = self.cleaned_data["capacidad"]
        if capacidad < 1:
            raise forms.ValidationError("La capacidad debe ser mayor que cero.")
        return capacidad
