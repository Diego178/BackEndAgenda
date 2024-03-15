from django.urls import path
from . import views

urlpatterns = [
    path('obtenerAsesor/', views.obtenerAsesoriasAsesor),
    path('obtenerUsuario/', views.obtenerAsesoriasUsuario),
    path('registrar/', views.registrarAsesoria),
    path('eliminar/', views.eliminarAsesoria),
]