from rest_framework.decorators import api_view
from rest_framework.response import Response

from ...models import Asesor, Curso
from ...serializers import CursoSerializer
from utils.validadores import es_valido_email, es_valido_matricula, es_valido_password
from ...models import Usuario
from ...serializers import UsuarioSerializer
from servicioAgenda.authentication import verificarTokenUsuario
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def registrarUsuario(request):
    # Obtener los datos de la peticion
    nombre = request.data.get('nombre')
    matricula = request.data.get('matricula')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if nombre is not None and matricula is not None and password is not None and email is not None:
        
        if not es_valido_matricula(matricula):
            return Response({'mensaje': 'La matricula no cumple los requisitos para que sea valida.', "error": True}, status=200)
        
        if not es_valido_email(email):
            return Response({'mensaje': 'Correo ingresado no valido.', "error": True}, status=200)
        
        if not es_valido_password(password):
            return Response({'mensaje': 'La contrasena no cumple los requisitos para que sea valida.', "error": True}, status=200)
        
        if Usuario.objects.filter(email=email).exists():
            return Response({'mensaje': 'Ya existe un usuario con este correo electronico registrado.', "error": True}, status=200)
        
        if Usuario.objects.filter(matricula=matricula).exists():
            return Response({'mensaje': 'Ya existe un usuario con esta matricula registrada.', "error": True}, status=200)
        
        password_encriptada = make_password(password)

        nuevo_usuario = Usuario(nombre=nombre, matricula=matricula, email=email, password=password_encriptada)

        nuevo_usuario.save()
   
        return Response({'mensaje': 'El usuario fue registrado correctamente.', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 
    
@api_view(['PUT'])
def actualizarUsuario(request):
    nombre = request.data.get('nombre')
    email = request.data.get('email')
    token = request.META.get('HTTP_AUTHORIZATION')


    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if nombre is not None  and email is not None:

        if not es_valido_email(email):
            return Response({'mensaje': 'Correo ingresado no valido.', "error": True}, status=200)
        
        try:
            usuario = Usuario.objects.get(id_usuario=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el usuario no existe en la base de datos.', "error": True}, status=200)
        

        usuario.nombre = nombre
        usuario.email = email

        usuario.save()
   
        return Response({'mensaje': 'Los datos del usuario fueron actualizados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)
    
@api_view(['POST'])
def obtenerDatosUsuario(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    usuario = Usuario.objects.get(id_usuario=mensaje)

    serializer = UsuarioSerializer(usuario)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['POST'])
def obtenerCursos(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    idAsesor = request.data.get('idAsesor')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesor = Asesor.objects.get(id_asesor=idAsesor)

    cursos = Curso.objects.filter(idasesor=asesor)

    serializer = CursoSerializer(cursos, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)
    