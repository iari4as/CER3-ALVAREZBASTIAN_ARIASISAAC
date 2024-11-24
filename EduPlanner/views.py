from datetime import datetime
import time
from django.shortcuts import render
from requests import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from core.models import Alerta, Evento as CoreEvento
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

            #prints de monitoreo
            #print("URL consultada:", response.url)
            #print("Código de respuesta:", response.status_code)
            #print("Cuerpo de la respuesta:", response.text)

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
        
class EventoValidationViewSet(ViewSet):
    """
    ViewSet para manejar la creación y validación de eventos académicos.
    """
    def create(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            fecha_inicio = serializer.validated_data['fecha_inicio']
            fecha_fin = serializer.validated_data['fecha_fin']
            titulo = serializer.validated_data['Titulo']

            # URL o consulta para obtener feriados desde el FeriadosViewSet
            url_api_feriados = "https://calendarific.com/api/v2/holidays"
            params = {
                "api_key": "dtcJZ596nMJrmn5Ev9Mzue4WDjxHGsdt",
                "country": "CL",
                "year": fecha_inicio.year,  # Solo obtenemos feriados del año correspondiente
            }

            try:
                # Consultar los feriados
                response = requests.get(url_api_feriados, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    feriados = data.get("response", {}).get("holidays", [])

                    # Convertir los feriados a objetos datetime para comparar
                    fechas_feriados = [
                        datetime.strptime(feriado["date"]["iso"], "%Y-%m-%d").date()
                        for feriado in feriados
                    ]

                    # Verificar si hay conflicto con algún feriado
                    conflicto = any(
                        fecha_inicio <= feriado <= fecha_fin for feriado in fechas_feriados
                    )

                    if conflicto:
                        # Crear alerta en core para que el administrador decida
                        Alerta.objects.create(
                            titulo="Conflicto entre evento y feriado",
                            descripcion=(
                                f"El evento '{titulo}' (del {fecha_inicio} al {fecha_fin}) "
                                f"coincide con un feriado. El administrador debe decidir qué hacer."
                            ),
                            tipo="ConflictoEvento",
                            estado="Pendiente"
                        )

                        return Response(
                            {
                                "message": (
                                    "El evento tiene conflicto con un feriado. "
                                    "Se ha enviado una alerta al administrador."
                                ),
                                "conflict": True
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            "message": "Error al consultar la API de feriados.",
                            "details": response.json()
                        },
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )
            except requests.exceptions.RequestException as e:
                return Response(
                    {
                        "message": "Error al conectar con la API de feriados.",
                        "error": str(e)
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            # Guardar el evento si no hay conflictos
            serializer.save()
            return Response({"message": "Evento creado exitosamente", "conflict": False}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventoViewSet(ModelViewSet):
    """
    ViewSet para manejar los eventos registrados en core.
    """
    queryset = CoreEvento.objects.all()
    serializer_class = EventoSerializer

    

