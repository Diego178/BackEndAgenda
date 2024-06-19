from rest_framework import serializers
from .models import Admin, Asesoria, Datosreunionvirtual, Diahora, Usuario, Asesor, Curso

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AsesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asesor
        fields = '__all__'



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
        
class AsesorSerializerGET(serializers.ModelSerializer):
    fotoBase64 = serializers.SerializerMethodField()

    class Meta:
        model = Asesor
        fields = ['id_asesor', 'nombre', 'idioma', 'fotoBase64']

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
        
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'nombre']
        
class AsesorSerializerGETAdmin(serializers.ModelSerializer):
    fotoBase64 = serializers.SerializerMethodField()
    num_asesorias = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Asesor
        fields = ['id_asesor', 'nombre', 'fotoBase64', 'idioma', 'email', 'num_asesorias']
    def get_fotoBase64(self, obj):
        if obj.fotoBase64:
            return obj.fotoBase64.decode('utf-8')
        return None