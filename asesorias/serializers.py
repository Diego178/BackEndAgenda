from rest_framework import serializers
from .models import Asesoria, Datosreunionvirtual, Diahora

class DatosReunionVirtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datosreunionvirtual
        fields = '__all__'


class AsesoriaSerializer(serializers.ModelSerializer):
    datos_reunion = DatosReunionVirtualSerializer(required=False)

    class Meta:
        model = Asesoria
        fields = '__all__'

class DiaHoraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diahora
        fields = '__all__'