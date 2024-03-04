from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario, Asesor
from .serializers import UsuarioSerializer, AsesorSerializer

@api_view(['POST'])
def login(request):
    # Obtener los datos de la peticion
    tipo = request.data.get('tipo')
    credencial = request.data.get('credencial')
    password = request.data.get('password')
    
    # Validar que no vengan nulos
    if tipo is not None and credencial is not None and password is not None:
        if(tipo != 'asesor' and tipo != 'usuario'):
            return Response({'mensaje': 'Tipo no valido', "error": True}, status=400)

        # Buscar al asesor
        try:
            if tipo == 'asesor':
                asesor = Asesor.objects.get(email=credencial, password=password)
                serializer = AsesorSerializer(asesor)
                # Devuelve el usuario encontrado en formato JSON
                return Response( {
                    'tipo': tipo,
                    'usuario': serializer.data,
                    "error": False}, status=200)
        except Asesor.DoesNotExist:
            # Si no se encuentra ningún usuario, devuelve un mensaje de error
            return Response({'mensaje': 'No se encontró ningún usuario con las credenciales proporcionadas', "error": True}, status=200)
            
        try:
            if tipo == 'usuario':
                usuario = Usuario.objects.get(matricula=credencial, password=password)
                serializer = UsuarioSerializer(usuario)
            # Devuelve el usuario encontrado en formato JSON
                return Response( {
                    'tipo': tipo,
                    'usuario': serializer.data,
                    "error": False}, status=200)
        except Usuario.DoesNotExist:
            # Si no se encuentra ningún usuario, devuelve un mensaje de error
            return Response({'mensaje': 'No se encontró ningún usuario con las credenciales proporcionadas', "error": True}, status=200)
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)  