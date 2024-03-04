from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asesor
from .serializers import AsesorSerializer
import re 

@api_view(['POST'])
def registrarAsesor(request):
    # Obtener los datos de la peticion
    nombre = request.data.get('nombre')
    idioma = request.data.get('idioma')
    email = request.data.get('email')
    password = request.data.get('password')

    if nombre is not None and idioma is not None and password is not None and email is not None:

        regexEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        regexPassword = r'^.{8,16}$'

        if not re.match(regexEmail, email):
            return Response({'mensaje': 'Correo ingresado no valido', "error": True}, status=200)
        
        if not re.match(regexPassword, password):
            return Response({'mensaje': 'La contrasena no cumple los requisitos para que sea valida', "error": True}, status=200)

        if Asesor.objects.filter(email=email).exists():
            return Response({'mensaje': 'Ya existe un asesor con este correo electrónico', "error": True}, status=200)
        
        nuevo_asesor = Asesor(nombre=nombre, idioma=idioma, email=email, password=password)

        nuevo_asesor.save()
   
        return Response({'mensaje': 'El asesor fue registrado correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)  

