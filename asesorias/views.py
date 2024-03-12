from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asesoria, Asesor, Diahora, Usuario
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AsesoriaSerializer
from utils.validadores import validar_fecha
from servicioAgenda.email import enviarCorreo
from utils.validadores import validar_fecha, obtenerDia
from servicioAgenda.authentication import verificarToken

import re

@api_view(['GET'])
def obtenerAsesoriasAsesor(request, id):
    # Obtener los datos de la peticion
    asesorias = Asesoria.objects.filter(idasesor=id)
    serializer = AsesoriaSerializer(asesorias, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def registrarAsesoria(request):
    # Obtener los datos de la peticion
    tipo = request.data.get('tipo')
    tema = request.data.get('tema')
    fecha = request.data.get('fecha')
    idAsesor = request.data.get('idAsesor')
    idDiaHora = request.data.get('idDiaHora')
    idUsuario = request.data.get('idUsuario')
    token = request.data.get('token')


    valido, mensaje = verificarToken(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)

    if tipo is not None and tema is not None and fecha is not None and idAsesor is not None and idDiaHora is not None and idUsuario is not None:
        if(tipo != 'asesoria' and tipo != 'oral'):
            return Response({'mensaje': 'Tipo no valido', "error": True}, status=400)
        
        if len(tema) > 200:
             return Response({'mensaje': 'Error, el tema supera el numero de caracteres.', "error": True}, status=200)
        
        if not validar_fecha(fecha):
             return Response({'mensaje': 'Error, la fecha no es valida.', "error": False}, status=200)
        
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
    idAsesoria = request.data.get('id_asesoria')
    token = request.data.get('token')

    valido, mensaje = verificarToken(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)

    try:
        asesoria_eliminar = Asesoria.objects.get(id_asesoria=idAsesoria)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'La asesoria que desea eliminar no existe', "error": False}, status=200) 


    usuario = Usuario.objects.get(id_usuario=asesoria_eliminar.idusuario.id_usuario)
 
    fecha = asesoria_eliminar.fecha
    enviarCorreo('Se elimino la asesoria del dia '+ obtenerDia(fecha.day) ,'La asesoria se elimino', usuario.email)

    return Response({'mensaje': 'Eliminado correctamente', "error": False}, status=200) 















