from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/autenticacion/', include('autenticacion.urls')),
    path('api/asesores/', include('asesores.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/asesorias/', include('asesorias.urls'))
]
