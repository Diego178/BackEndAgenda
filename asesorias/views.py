from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asesoria, Asesor, Diahora, Usuario
from django.core.exceptions import ObjectDoesNotExist
from utils.validadores import validar_fecha
from servicioAgenda.email import enviarCorreo

import re

@api_view(['POST'])
def registrarAsesoria(request):
    # Obtener los datos de la peticion
    tipo = request.data.get('tipo')
    tema = request.data.get('tema')
    fecha = request.data.get('fecha')
    idAsesor = request.data.get('idAsesor')
    idDiaHora = request.data.get('idDiaHora')
    idUsuario = request.data.get('idUsuario')

    if tipo is not None and tema is not None and fecha is not None and idAsesor is not None and idDiaHora is not None and idUsuario is not None:

        if len(tema) > 200:
             return Response({'mensaje': 'Error, el tema supera el numero de caracteres.', "error": True}, status=200)
        try:
            asesor = Asesor.objects.get(id_asesor=idAsesor)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        
        try:
            diaHora= Diahora.objects.get(id_diahora=idDiaHora)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el horario elegido no existe en la base de datos.', "error": True}, status=200)
        
        try:
            usuario = Usuario.objects.get(id_usuario=idUsuario)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el usuario no existe en la base de datos.', "error": True}, status=200)
        
        nueva_asesoria = Asesoria(tipo=tipo, tema=tema, fecha=fecha, idasesor=asesor, iddiahora= diaHora, idusuario=usuario)


        nueva_asesoria.save()
   
        return Response({'mensaje': 'El usuario fue registrado correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 
    
@api_view(['DELETE'])
def eliminarAsesoria(request):
    # Obtener los datos de la peticion
    idAsesoria = request.data.get('nombre')
    matricula = request.data.get('matricula')
    email = request.data.get('email')
    password = request.data.get('password')

    enviarCorreo('fabriii', 'afabri24@gmail.com')

    return Response({'mensaje': 'Eliminado correctamente', "error": False}, status=200) 










