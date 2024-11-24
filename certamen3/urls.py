"""
URL configuration for certamen3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core.views import home, iniciarSesion,manageEvents,signout,registroUser, event_form,editar_evento\
                    , eliminar_evento, guardar_edit
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name="home" ),
    path('login/', iniciarSesion, name="login"),
    path('Eventos/', manageEvents, name="ManageEvents"),
    path('registro/', registroUser, name= "register"),
    path('logout/', signout, name="logout"),
    path('CrearEvento/', event_form, name="event_form"),
    path('eliminar_evento/<int:evento_id>/', eliminar_evento, name='eliminar_evento'),
    path('editar_evento/<int:evento_id>/', editar_evento, name='editar_evento'),
    path('confirm/', guardar_edit, name='guardar_edit'),
    path('api/', include('EduPlanner.urls')),
]
