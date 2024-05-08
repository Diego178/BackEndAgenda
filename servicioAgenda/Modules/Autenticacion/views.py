from rest_framework.decorators import api_view
from rest_framework.response import Response

from servicioAgenda.authentication import crearToken
from ...models import Usuario, Asesor
from ...serializers import UsuarioSerializer, AsesorSerializer



from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def login(request):
    # Obtener los datos de la peticion
    tipo = request.data.get('tipo')
    credencial = request.data.get('credencial')
    contrasenia = request.data.get('password')
    
    
    # Validar que no vengan nulos
    if tipo is not None and credencial is not None and contrasenia is not None:
        if(tipo != 'asesor' and tipo != 'usuario'):
            return Response({'mensaje': 'Tipo no valido', "error": True}, status=400)

        # Buscar al asesor
        if tipo == 'asesor':
            try:
                asesor = Asesor.objects.get(email=credencial)
                if check_password(contrasenia, asesor.password):
                    serializer = AsesorSerializer(asesor)
                    return Response( {
                        'tipo': tipo,
                        'usuario': serializer.data,
                        'token': crearToken(asesor.id_asesor, tipo),
                        "error": False}, status=200)
            except Asesor.DoesNotExist:
                return Response({'mensaje': 'No se encontró ningún asesor con las credenciales proporcionadas', "error": True}, status=200)
            except Exception as e:
                return Response({'mensaje': 'Ocurrió un error inesperado: {}'.format(e), "error": True}, status=500)
        elif tipo == 'usuario':
            try:
                usuario = Usuario.objects.get(matricula=credencial)
            except Usuario.DoesNotExist:
                return Response({'mensaje': 'No se encontró ningún usuario con la matrícula proporcionada', "error": True}, status=400)
            
            # Verificar la contraseña
            if not check_password(contrasenia, usuario.password):
                return Response({'mensaje': 'Contraseña incorrecta', "error": True}, status=400)
            
            # No necesitas verificar la contraseña aquí si solo estás intentando obtener el usuario
            serializer = UsuarioSerializer(usuario)
            return Response({
                'tipo': tipo,
                'usuario': serializer.data,
                'token': crearToken(usuario.id_usuario, tipo),
                "error": False}, status=200)
            