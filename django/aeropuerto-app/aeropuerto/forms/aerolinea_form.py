from django import forms

from aeropuerto.models import Aerolinea


class AerolineaForm(forms.ModelForm):
    class Meta:
        model = Aerolinea
        fields = ["codigo", "nombre", "pais_origen"]
        widgets = {"codigo": forms.TextInput(attrs={"maxlength": 3})}

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip().upper()
        if len(codigo) != 3 or not codigo.isalpha():
            raise forms.ValidationError("El código debe tener tres letras.")
        return codigo
