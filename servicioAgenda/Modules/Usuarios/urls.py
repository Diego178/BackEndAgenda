from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrarUsuario),
    path('actualizar/', views.actualizarUsuario),
    path('obtenerDatosUsuario/', views.obtenerDatosUsuario),
    path('obtenerCursos/', views.obtenerCursos),
    path('obtenerIdiomas/', views.obtenerIdiomas),
    path('agregarIdioma/', views.agregarIdioma),
    path('eliminarIdioma/', views.eliminarIdioma),
    path('recuperarContrasena/', views.cambiarContrasena),
]