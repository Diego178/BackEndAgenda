from rest_framework.decorators import api_view
from rest_framework.response import Response

from servicioAgenda.authentication import crearToken, crearTokenAdmin
from ...models import Admin, Usuario, Asesor
from ...serializers import AdminSerializer, UsuarioSerializer, AsesorSerializer
from servicioAgenda.email import enviarCorreoRecuperacion



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
            
@api_view(['POST'])
def loginAdmin(request):
    # Obtener los datos de la peticion
    email = request.data.get('email')
    password = request.data.get('password')
    # Validar que no vengan nulos
    if email is not None and password is not None:
        try:
            admin = Admin.objects.get(email=email, password=password)
            print(admin.nombre)
            serializer = AdminSerializer(admin)
            return Response( {
                'tipo': 'admin',
                'usuario': serializer.data,
                'token': crearTokenAdmin(admin.id),
                "error": False}, status=200)
        except Admin.DoesNotExist:
                return Response({'mensaje': 'No se encontró ningúna cuenta con las credenciales proporcionadas', "error": True}, status=200)
        except Exception as e:
            return Response({'mensaje': 'Ocurrió un error inesperado: {}'.format(e), "error": True}, status=500)
        
#Aqui va el codigo de recuperar la contraseña
@api_view(['POST'])
def recuperarContrasenia(request):
    email = request.data.get('email')
    if email is not None:
        try:
            usuario = Usuario.objects.get(email=email)
            enviarCorreoRecuperacion(email,usuario.id_usuario)
            return Response({'mensaje': 'Se ha enviado un correo con las instrucciones para recuperar tu contraseña', "error": False}, status=200)
        except Usuario.DoesNotExist:
            return Response({'mensaje': 'No se encontró ningún usuario con el correo proporcionado', "error": True}, status=400)
        except Exception as e:
            return Response({'mensaje': 'Ocurrió un error inesperado: {}'.format(e), "error": True}, status=500)


