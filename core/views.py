from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
import re
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.serializers import EventoSerializer

from .models import Evento
from .forms import FormularioEvento
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages


def verificar_fechas(fecha_inicio, fecha_termino, fechas_lista):
    for fecha in fechas_lista:
        # Si la fecha está en el rango o es igual a la fecha de inicio o fin, retornamos 0
        if fecha_inicio <= fecha <= fecha_termino:
            print(f"Fecha {fecha.strftime('%Y-%m-%d')} está dentro del rango o es inicio/fin, retornando 0")
            return 0
    print("No hay fechas dentro del rango.")
    return 1  # Si no se encuentra ninguna fecha dentro del rango


@login_required
def manageEvents(request):
    if request.user.groups.filter(name='AdministradorAcademico').exists():
        eventos = Evento.objects.all()
        return render(request, 'core/manage_events.html', {'eventos': eventos})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

# Create your views here.
import requests
from django.shortcuts import render

def home(request):
    # Obtener el tipo de evento desde el filtro de la URL (si está presente)
    event_type_filter = request.GET.get('event_type', '')

    # Filtrar los eventos según el tipo, si es necesario
    if event_type_filter:
        eventos = Evento.objects.filter(TipoEvento=event_type_filter)
    else:
        eventos = Evento.objects.all()  # Si no hay filtro, mostrar todos los eventos

    # Realizar la solicitud GET para obtener los feriados
    feriados_url = 'http://127.0.0.1:8000/api/Feriados/'  # URL de la API de feriados
    feriados_response = requests.get(feriados_url)
    

    # Verificar si la solicitud fue exitosa
    if feriados_response.status_code == 200:
        feriados = feriados_response.json()  # Obtenemos los feriados como un diccionario

        
    else:
        feriados = []  # Si la solicitud falla, devolvemos una lista vacía

    # Crear el diccionario de contexto
    data = {
        'eventos': eventos,
        'TIPO_EVENTO_CHOICES': Evento.TIPO_EVENTO_CHOICES,
        'feriados': feriados,  # Añadir los feriados al contexto
    }

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


def get_events(request):
    # Obtener los eventos locales desde la base de datos
    eventos = Evento.objects.all()
    eventos_list = [
        {
            "title": evento.Titulo,
            "start": evento.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),
            "end": evento.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'),
            "description": evento.Descripcion,
            "type": evento.TipoEvento,
        }
        for evento in eventos
    ]

    # Obtener feriados de Calendarific
    feriados_url = 'http://127.0.0.1:8000/api/Feriados/'
    feriados_response = requests.get(feriados_url)

    if feriados_response.status_code == 200:
        feriados = feriados_response.json()
        feriados_list = [
            {
                "title": feriado['name'],
                "start": feriado['date']['iso'],
                "description": feriado.get('description', 'Feriado oficial'),
                "backgroundColor": "#FF5733", 
                "borderColor": "#C70039",
            }
            for feriado in feriados.get('feriados', [])
        ]
        eventos_list.extend(feriados_list)
    return JsonResponse(eventos_list, safe=False)


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

def es_administrador(usuario):
    return usuario.is_authenticated and usuario.groups.filter(name="AdministradorAcademico").exists()

@user_passes_test(es_administrador)
def event_form(request):
    errors = {}
    # Realizar la solicitud GET para obtener los feriados
    feriados_url = 'http://127.0.0.1:8000/api/Feriados/'  # URL de la API de feriados
    feriados_response = requests.get(feriados_url)
     # Verificar si la solicitud fue exitosa
    if feriados_response.status_code == 200:
        feriados = feriados_response.json()  # Obtenemos los feriados como un diccionario
    else:
        feriados = []  # Si la solicitud falla, devolvemos una lista vacía

    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        start_date = request.POST.get("start_date", "")
        
        end_date = request.POST.get("end_date", "")
        event_type = request.POST.get("event_type", "")
        lista_fechas = []
        for f in feriados['feriados']:   
            fecha = datetime(f['date']['datetime']['year'], f['date']['datetime']['month'], f['date']['datetime']['day'])
            lista_fechas.append(fecha)



        fecha_inicioDatatime= datetime.strptime(start_date,"%Y-%m-%d")
        fecha_finDatatime= datetime.strptime(end_date,"%Y-%m-%d")
        if  verificar_fechas(fecha_inicioDatatime, fecha_finDatatime, lista_fechas):
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
                if start_date_obj > end_date_obj:
                    errors["dates"] = "La fecha de inicio debe ser anterior a la fecha de fin."
            except ValueError:
                errors["dates"] = "Las fechas deben tener un formato válido."

            # Validación del tipo de evento
            if not event_type:
                errors["event_type"] = "Debes seleccionar un tipo de evento."
        else:
            errors["dates"] = "Error, uno o varios dias este rango de fechas corresponde a feriados"
    

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


