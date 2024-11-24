from rest_framework import routers
from .views import EventoValidationViewSet, FeriadosViewSet, EventoViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register('Feriados', FeriadosViewSet, basename='feriados')
router.register('Eventos/validacion', EventoValidationViewSet, basename='evento-validacion')
router.register('Eventos', EventoViewSet, basename='eventos')

urlpatterns = [
    path('', include(router.urls)),
]