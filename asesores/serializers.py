from rest_framework import serializers
from .models import Asesor, Curso, Datosreunionvirtual

class AsesorSerializer(serializers.ModelSerializer):
    fotoBase64 = serializers.SerializerMethodField()

    class Meta:
        model = Asesor
        fields = ['nombre', 'idioma', 'email', 'password', 'fotoBase64']

    def get_fotoBase64(self, obj):
        if obj.fotoBase64:
            return obj.fotoBase64.decode('utf-8')
        return None

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class DatosReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datosreunionvirtual
        fields = '__all__'