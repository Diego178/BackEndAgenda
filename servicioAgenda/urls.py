from django.contrib import admin
from django.urls import path, include
from .reporte import ReporteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/autenticacion/', include('autenticacion.urls')),
    path('api/asesores/', include('asesores.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/asesorias/', include('asesorias.urls')),
    path('reporte/', ReporteView.as_view(), name='reporte')
]
