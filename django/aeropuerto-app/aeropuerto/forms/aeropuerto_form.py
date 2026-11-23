from django import forms

from aeropuerto.models import Aeropuerto


class AeropuertoForm(forms.ModelForm):
    class Meta:
        model = Aeropuerto
        fields = ["codigo_iata", "nombre", "ciudad", "pais", "aerolineas"]
        widgets = {
            "codigo_iata": forms.TextInput(attrs={"maxlength": 3}),
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre del aeropuerto"}),
            "aerolineas": forms.CheckboxSelectMultiple(),
        }

    def clean_codigo_iata(self):
        codigo = self.cleaned_data["codigo_iata"].strip().upper()
        if len(codigo) != 3 or not codigo.isalpha():
            raise forms.ValidationError("El código IATA debe tener tres letras.")
        return codigo
