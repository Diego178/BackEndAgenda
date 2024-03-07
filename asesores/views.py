from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asesor, Datosreunionvirtual, Diahora
from utils.validadores import es_dia_semana, es_hora_valida, es_valido_modalidad
from django.core.exceptions import ObjectDoesNotExist
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


@api_view(['POST'])
def registrarDatosReunionVirtual(request):

    url = request.data.get('url')
    password = request.data.get('password')
    id_reunion = request.data.get('id_reunion')
    idAsesor = request.data.get('idAsesor')

    if url is not None and id_reunion is not None and password is not None and idAsesor is not None:
        regexURL = r'^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$'

        if not re.match(regexURL, url):
            return Response({'mensaje': 'El enlace para la reunion virtual no es valido', "error": True}, status=200)
        
        if Datosreunionvirtual.objects.filter(idasesor=idAsesor).exists():
            return Response({'mensaje': 'Error el asesor ya cuenta con datos para su reunion virtual.', "error": True}, status=200)
        try:
            asesor = Asesor.objects.get(id_asesor=idAsesor)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)    
            
        nuevo_datos = Datosreunionvirtual(url=url, password=password, id_reunion=id_reunion, idasesor=asesor)

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos de la reunion fueron registrados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)
    

@api_view(['POST'])
def registrarDiaHora(request):
    dia = request.data.get('dia')
    hora_inicio = request.data.get('hora_inicio')
    hora_termino = request.data.get('hora_termino')
    modalidad = request.data.get('modalidad')
    idAsesor = request.data.get('idAsesor')

    if dia is not None and hora_inicio is not None and hora_termino is not None and modalidad is not None and idAsesor is not None:
        
        try:
            asesor = Asesor.objects.get(id_asesor=idAsesor)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        

        if not es_dia_semana(dia):
             return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": False}, status=200)
        
        if not es_hora_valida(hora_inicio):
             return Response({'mensaje': 'Error, la hora de inicio no es valida.', "error": False}, status=200)
        
        if not es_hora_valida(hora_termino):
             return Response({'mensaje': 'Error, la hora de termino no es valida.', "error": False}, status=200)
            
        nuevo_datos = Diahora(dia=dia, hora_inicio=hora_inicio, hora_termino=hora_termino, modalidad=modalidad, idasesor=asesor, eslibre=True, estado="disponible")

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos de la reunion fueron registrados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)
    
@api_view(['PUT'])
def actuaizarHoraDia(request):
    id_dia_hora = request.data.get('idDiaHora')
    dia = request.data.get('dia')
    hora_inicio = request.data.get('hora_inicio')
    hora_termino = request.data.get('hora_termino')
    modalidad = request.data.get('modalidad')
    estado = request.data.get('estado')
    es_libre = request.data.get('esLibre')
    id_asesor = request.data.get('idAsesor')

    if id_dia_hora is not None and dia is not None and hora_inicio is not None and hora_termino is not None and modalidad is not None and id_asesor is not None and estado is not None and es_libre is not None:
        
        try:
            asesor = Asesor.objects.get(id_asesor=id_asesor)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        
        if not es_dia_semana(dia):
             return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": False}, status=200)
        
        if not es_hora_valida(hora_inicio):
             return Response({'mensaje': 'Error, la hora de inicio no es valida.', "error": False}, status=200)
        
        if not es_hora_valida(hora_termino):
             return Response({'mensaje': 'Error, la hora de termino no es valida.', "error": False}, status=200)
            
        if not es_valido_modalidad(modalidad):
             return Response({'mensaje': 'Error, la modalidad no es valida.', "error": False}, status=200)
        
        nuevo_datos = Diahora(id_diahora=id_dia_hora, dia=dia, hora_inicio=hora_inicio, hora_termino=hora_termino, modalidad=modalidad, idasesor=asesor, eslibre=es_libre, estado=estado)

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos de la reunion fueron actualizados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)

