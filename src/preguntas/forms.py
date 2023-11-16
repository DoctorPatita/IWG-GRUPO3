from django import forms
from .models import Pregunta, Respuesta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['titulo', 'contenido']

class RespuestaForm(forms.ModelForm):
    contenido = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    class Meta:
        model = Respuesta
        fields = ['contenido']

