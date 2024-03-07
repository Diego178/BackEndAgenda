from django.urls import path
from . import views

urlpatterns = [
    path('obtenerAsesor/<int:id>/', views.obtenerAsesoriasAsesor),
    path('registrar/', views.registrarAsesoria),
    path('eliminar/', views.eliminarAsesoria),
]