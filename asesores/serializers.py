from rest_framework import serializers
from .models import Asesor, Curso, Datosreunionvirtual

class AsesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asesor
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class DatosReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datosreunionvirtual
        fields = '__all__'