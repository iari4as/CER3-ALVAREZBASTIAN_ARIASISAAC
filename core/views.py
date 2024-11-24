from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
import re
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EventoSerializer
from .models import Evento
from .forms import FormularioEvento
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages


@login_required
def manageEvents(request):
    if request.user.groups.filter(name='AdministradorAcademico').exists():
        eventos = Evento.objects.all()
        return render(request, 'core/manage_events.html', {'eventos': eventos})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

# Create your views here.
def home(request):
    eventos = Evento.objects.all()  # Obtener todos los eventos
    
    # Intentamos obtener los feriados desde la API

    # Creamos el diccionario con los datos para el contexto
    data = {
        'eventos': eventos,
    }
    
    # Retornamos la respuesta renderizada con los datos
    return render(request, "core/index.html", data)

def iniciarSesion(request):
        data = {
            'form':UserCreationForm
        }
    
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        flag = True

        
        if(request.method == 'GET'):
            return render(request, 'core/login.html',data)
        else:
            #################### VALIDACIONES ##########################
            if(len(username) == 0 or len(password1) == 0):
                flag = False
            ############################################################
            print(flag)
            if(flag):
                    
                print(request.POST)
                user = authenticate(request, username= request.POST['username'], password=request.POST['password1'])
            
                if user is None:
                    data = {
                        'form':UserCreationForm,
                        'error1': ' usuario o contraseña incorrectas'
                    }
                else:
                    login(request, user)
                    return redirect(home)
            else:
                data = {
                    'form':UserCreationForm,
                    'error2':' debe ingresar informacion en ambos campos'
                }
        return render(request, 'core/login.html', data) 



def registroUser(request):
    data = {
            'form':UserCreationForm
        }

    email = request.POST.get('email', '')
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    username = request.POST.get('username', '')
    role = request.POST.get('role','')
    flag = True

    
    if(request.method == 'GET'):
        return render(request, 'core/register.html',data)
    else:
        #################### VALIDACIONES ##########################
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if( not re.match(email_regex,email ) or 
            ((len(email) == 0 )or 
            (len(password2) == 0) and 
            (len(password1) == 0) or  
            (len(username) == 0) or
            (len(role) == 0))):
            flag = False
        ############################################################
        print(password1 + " " + password2 +" " +username +" "+ role)
        if(flag):
            
            if(request.POST['password1'] == request.POST['password2'] ):
                try:
                    user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'], password=request.POST['password1'])

                    user.save()
                    login(request, user)
                    return redirect("home")
                    
                except:
                    data = {
                        'form':UserCreationForm,
                        'error1': 'Nombre de usuario ya existe, intenta otro'
                    }
                    return render(request, 'core/register.html', data)
            data = {
                'form':UserCreationForm,
                'error2': 'Las contraseñas no coinciden'
            }
            return  render(request, 'core/register.html', data)
        else:
            data = {
                'form':UserCreationForm,
                'error3': 'Llene todos los campos requeridos'
            }
            return  render(request, 'core/register.html', data)
        


def signout(request):
        logout(request)
        return redirect('home')

from django.shortcuts import render, redirect
from .models import Evento
from datetime import datetime

def event_form(request):
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        event_type = request.POST.get("event_type", "")

        # Validación del título
        if len(title) < 5:
            errors["title"] = "El título debe tener al menos 5 caracteres."

        # Validación de la descripción
        if len(description) < 10:
            errors["description"] = "La descripción debe tener al menos 10 caracteres."

        # Validación de las fechas
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date_obj >= end_date_obj:
                errors["dates"] = "La fecha de inicio debe ser anterior a la fecha de fin."
        except ValueError:
            errors["dates"] = "Las fechas deben tener un formato válido."

        # Validación del tipo de evento
        if not event_type:
            errors["event_type"] = "Debes seleccionar un tipo de evento."

        # Si hay errores, se devuelven al formulario
        if errors:
            data = {
                'errors': errors,
                'TIPO_EVENTO_CHOICES': Evento.TIPO_EVENTO_CHOICES,
            }
            return render(request, "core/event_form.html", data)

        # Si no hay errores, guardar el evento
        evento = Evento(
            Titulo=title,
            Descripcion=description,
            fecha_inicio=start_date_obj,
            fecha_fin=end_date_obj,
            TipoEvento=event_type
        )
        evento.save()
        return redirect("ManageEvents")  # Redirigir a la página correspondiente

    # Si la solicitud no es POST, solo renderizamos el formulario
    data = {
        'errors': errors,
        'TIPO_EVENTO_CHOICES': Evento.TIPO_EVENTO_CHOICES,
    }
    return render(request, "core/event_form.html", data)


class EventoAPI(APIView):
    def post(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            # Llamar a la API de Calendarific
            fecha_inicio = serializer.validated_data['fecha_inicio']
            year = fecha_inicio.year  # Extraer el año de la fecha
            api_key = "TU_API_KEY" 
            url_api_feriados = f"https://calendarific.com/api/v2/holidays"
            params = {
                "api_key": api_key,
                "country": "CL",
                "year": year,
                "type": "national"
            }
            
            try:
                response = requests.get(url_api_feriados, params=params)
                if response.status_code == 200:
                    data = response.json()
                    holidays = data.get('response', {}).get('holidays', [])
                    es_feriado = any(
                        holiday['date']['iso'] == str(fecha_inicio) for holiday in holidays
                    )
                    if es_feriado:
                        return Response(
                            {"message": "La fecha coincide con un feriado en Chile.", "conflict": True},
                            status=status.HTTP_400_BAD_REQUEST
                        )
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
            
            # Guardar el evento si no hay conflictos
            serializer.save()
            return Response({"message": "Evento creado exitosamente", "conflict": False}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def eliminar_evento(request, evento_id):
    if request.method == "POST":
        evento = get_object_or_404(Evento, id=evento_id)
        evento.delete()
        messages.success(request, "El evento fue eliminado exitosamente.")
    return redirect('ManageEvents')  # Cambia 'lista_eventos' por la vista correspondiente.


def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == "POST":
        evento.Titulo = request.POST.get('title')
        evento.Descripcion = request.POST.get('description')
        evento.fecha_inicio = request.POST.get('start_date')
        evento.fecha_fin = request.POST.get('end_date')
        evento.TipoEvento = request.POST.get('event_type')
        evento.save()
        return redirect('ManageEvents')
    return render(request, 'core/edit_evento.html', {
        'evento': evento,
        'TIPO_EVENTO_CHOICES': Evento.TIPO_EVENTO_CHOICES,
    })

@login_required
def gestioneventos(request):
    eventos = Evento.objects.all()
    if request.method == 'POST':
        evento_id = request.POST.get('event_id', None)
        if evento_id: 
            evento = get_object_or_404(Evento, id=evento_id)
            form = FormularioEvento(request.POST, instance=evento)
        else:
            form = FormularioEvento(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = FormularioEvento()
    return render(request, "core/manage_events.html", {
        'eventos': eventos,
        'form': form
    })



def guardar_edit(request):
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        nuevoTipo = request.POST.get('event_type')
        titulo = request.POST.get('title')
        fechaInicio = request.POST.get('start_date')
        fechaFin = request.POST.get('end_date')
        descripcion = request.POST.get('description')
        evento = Evento.objects.get(id = evento_id)
        evento.Descripcion = descripcion
        evento.TipoEvento = nuevoTipo
        evento.Titulo = titulo
        evento.fecha_inicio = fechaInicio
        evento.fecha_fin = fechaFin
        evento.save()
        return redirect('ManageEvents')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evento
from .serializers import EventoSerializer

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
