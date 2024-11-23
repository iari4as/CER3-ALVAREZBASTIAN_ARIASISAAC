from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, "core/index.html")

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

def manageEvents(request):
    return render(request, "core/manage_events.html")

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