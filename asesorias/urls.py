from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrarAsesoria),
    path('eliminar/', views.eliminarAsesoria),
]