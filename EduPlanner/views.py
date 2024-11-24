import time
from django.shortcuts import render
from requests import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from core.models import Evento as CoreEvento
import requests

from EduPlanner.serializers import EventoSerializer

class FeriadosViewSet(ViewSet):
    """
    ViewSet para obtener los feriados desde la API de Calendarific.
    """
    def list(self, request):
        # Define la URL base y tus credenciales de API
        api_key = "dtcJZ596nMJrmn5Ev9Mzue4WDjxHGsdt"
        url_api_calendarific = "https://calendarific.com/api/v2/holidays"

        # Configura los parámetros necesarios
        params = {
            "api_key": api_key,
            "country": "CL",  # Código de país para Chile
            "year": 2024
        }

        try:
            # Realiza la solicitud a la API de Calendarific
            response = requests.get(url_api_calendarific, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                feriados = data.get("response", {}).get("holidays", [])
                return Response({"feriados": feriados}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Error al consultar la API de Calendarific.", "details": response.json()},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"message": "Error al conectar con la API de Calendarific.", "error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
class EventoViewSet(ViewSet):
    """
    ViewSet para manejar la creación y validación de eventos.
    """
    def create(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            fecha_inicio = serializer.validated_data['fecha_inicio']
            fecha_fin = serializer.validated_data['fecha_fin']

            # Validar si la fecha de inicio o fin se solapa con eventos existentes
            conflicto = CoreEvento.objects.filter(
                fecha_inicio__lte=fecha_fin,  # Inicio existente antes o igual al fin nuevo
                fecha_fin__gte=fecha_inicio   # Fin existente después o igual al inicio nuevo
            ).exists()

            if conflicto:
                return Response(
                    {"message": "El rango de fechas coincide con otro evento registrado.", "conflict": True},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Si no hay conflictos, guarda el nuevo evento
            serializer.save()
            return Response({"message": "Evento creado exitosamente", "conflict": False}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventoViewSet(ModelViewSet):
    """
    ViewSet para manejar los eventos registrados en core.
    """
    queryset = CoreEvento.objects.all()
    serializer_class = EventoSerializer
    

class EventoCreateAPIView(APIView):
    """
    API para crear eventos.
    """

    def post(self, request, *args, **kwargs):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
