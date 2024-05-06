from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from .reporte import ReporteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/autenticacion/', include('autenticacion.urls')),
    path('api/asesores/', include('asesores.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/asesorias/', include('asesorias.urls')),
    #path('reporte/', ReporteView.as_view(), name='reporte')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)