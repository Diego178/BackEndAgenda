from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrarUsuario),
    path('actualizar/', views.actualizarUsuario),
    path('obtenerDatosUsuario/', views.obtenerDatosUsuario),
]