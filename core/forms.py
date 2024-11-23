from django import forms
from .models import EventoAcademico

class FormularioEvento(forms.ModelForm):
    class Meta:
        model = EventoAcademico
        fields = ['Titulo', 'Descripcion', 'InicioPeriodo', 'FinPeriodo', 'TipoEvento']