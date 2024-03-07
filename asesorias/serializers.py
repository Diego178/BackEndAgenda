from rest_framework import serializers
from .models import Asesoria

class AsesoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asesoria
        fields = '__all__'