from django.urls import path
from . import views

urlpatterns = [
    path("obtenerAsesores/", views.obtenerAsesores)
]