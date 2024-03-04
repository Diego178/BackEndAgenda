from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
import re 

@api_view(['POST'])
def registrarUsuario(request):
    # Obtener los datos de la peticion
    nombre = request.data.get('nombre')
    matricula = request.data.get('matricula')
    email = request.data.get('email')
    password = request.data.get('password')

    if nombre is not None and matricula is not None and password is not None and email is not None:
        
        regexMatricula = r'S\d{8}'
        regexEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        regexPassword = r'^.{8,16}$'

        if not re.match(regexMatricula, matricula):
            return Response({'mensaje': 'La matricula no cumple los requisitos para que sea valida', "error": True}, status=200)
        
        if not re.match(regexEmail, email):
            return Response({'mensaje': 'Correo ingresado no valido', "error": True}, status=200)
        
        if not re.match(regexPassword, password):
            return Response({'mensaje': 'La contrasena no cumple los requisitos para que sea valida', "error": True}, status=200)
        
        if Usuario.objects.filter(email=email).exists() and Usuario.objects.filter(matricula=matricula).exists():
            return Response({'mensaje': 'Ya existe un usuario con estas credenciales', "error": True}, status=200)
        
        nuevo_usuario = Usuario(nombre=nombre, matricula=matricula, email=email, password=password)

        nuevo_usuario.save()
   
        return Response({'mensaje': 'El usuario fue registrado correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 