from rest_framework import routers
from .views import EventoViewSet, FeriadosViewSet  
from django.urls import include, path

router = routers.DefaultRouter()
router.register('Feriados', FeriadosViewSet, basename='feriados')
router.register('Eventos', EventoViewSet, basename='eventos')

urlpatterns = [
    path('', include(router.urls)),
]