from django.urls import path
from . import views

urlpatterns = [
    path("obtenerAsesores/", views.obtenerAsesores),
    path("actualizarAsesor/", views.actualizarAsesor),
    path("obtenerUsuarios/", views.obtenerUsuarios),
    path("actualizarUsuario/", views.actualizarUsuario),
    path('obtenerAdmins/', views.obtenerAdmins),
    path('registrarAdmin/', views.registrarAdministrador),
    path('actualizarAdmin/', views.actualizarAdmin),
    path('estadoAsesor/', views.estadoAsesor)
]