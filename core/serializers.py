from rest_framework import serializers
from .models import EventoAcademico

class SerializadorEventos(serializers.ModelSerializer):
    class Meta:
        model = EventoAcademico
        fields = '__all__'

    def validate(self, data):
        if data['InicioPeriodo'] > data['FinPeriodo']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
        return data