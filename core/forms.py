from django import forms
from .models import Evento

class FormularioEvento(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['Titulo', 'Descripcion', 'fecha_inicio', 'fecha_fin', 'TipoEvento']