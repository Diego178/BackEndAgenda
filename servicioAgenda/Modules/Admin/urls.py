from django.urls import path
from . import views

urlpatterns = [
    path("obtenerAsesores/", views.obtenerAsesores),
    path("actualizarAsesor/", views.actualizarAsesor)
]