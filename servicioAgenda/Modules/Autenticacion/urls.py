from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('admin/', views.loginAdmin),
    path('recuperar-contrasena/', views.recuperarContrasenia)
]