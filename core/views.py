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