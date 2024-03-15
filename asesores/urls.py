from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrarAsesor),
    path('registrarDatosReunion/', views.registrarDatosReunionVirtual),
    path('registrarDiaHora/', views.registrarDiaHora),
    path('actualizarDiaHora/', views.actuaizarHoraDia),
    path('eliminarDiaHora/', views.eliminarHoraDia),
    path('obtenerDatosAsesor/', views.obtenerDatosAsesor),
]