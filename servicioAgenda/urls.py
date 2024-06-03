from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from .reporte import ReporteView

from .Modules.Autenticacion import urls as autenticacion_urls
from .Modules.Asesorias import urls as asesorias_urls
from .Modules.Asesores import urls as asesores_urls
from .Modules.Usuarios import urls as usuarios_urls
from .Modules.Admin import urls as admin_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/autenticacion/', include(autenticacion_urls)),
    path('api/asesores/', include(asesores_urls)),
    path('api/usuarios/', include(usuarios_urls)),
    path('api/asesorias/', include(asesorias_urls)),
    path('api/admin/', include(admin_urls)),
    #path('reporte/', ReporteView.as_view(), name='reporte')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)