from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Asesoria, Asesor, Diahora, Usuario, Datosreunionvirtual
from django.core.exceptions import ObjectDoesNotExist
from .serializers import DiaHoraSerializer
from utils.validadores import es_dia_semana, validar_fecha
from servicioAgenda.email import enviarCorreo
from utils.validadores import validar_fecha, obtenerDia
from servicioAgenda.authentication import verificarToken, verificarTokenAsesor, verificarTokenUsuario


@api_view(['POST'])
def obtenerAsesoriasAsesor(request):
    # Obtener los datos de la peticion
    token = request.data.get('token')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)
    
    asesorias = Asesoria.objects.filter(idasesor=mensaje)
    data = []
    for asesoria in asesorias:
        if asesoria.tipo == 'virtual':
            datos_reunion = Datosreunionvirtual.objects.get(idasesor=asesoria.idasesor)
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_usuario': asesoria.idusuario.nombre,
                'fecha': asesoria.fecha,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino,
                'password_reunion': datos_reunion.password,
                'url_reunion': datos_reunion.url,
                'id_reunion': datos_reunion.id_reunion
            }
            data.append(asesoria_data)
        else:
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_usuario': asesoria.idusuario.nombre,
                'fecha': asesoria.fecha,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino
            }
            data.append(asesoria_data)

    return Response(data, status=200)


@api_view(['POST'])
def obtenerAsesoriasUsuario(request):
    # Obtener los datos de la peticion
    token = request.data.get('token')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)
    
    asesorias = Asesoria.objects.filter(idusuario=mensaje)
    data = []
    for asesoria in asesorias:
        if asesoria.tipo == 'virtual':
            datos_reunion = Datosreunionvirtual.objects.get(idasesor=asesoria.idasesor)
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_asesor': asesoria.idasesor.nombre,
                'fecha': asesoria.fecha,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino,
                'password_reunion': datos_reunion.password,
                'url_reunion': datos_reunion.url,
                'id_reunion': datos_reunion.id_reunion
            }
            data.append(asesoria_data)
        else:
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_asesor': asesoria.idasesor.nombre,
                'fecha': asesoria.fecha,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino
            }
            data.append(asesoria_data)

    return Response(data, status=200)


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
   
        return Response({'mensaje': 'La asesoria fue registrada correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 
    
@api_view(['DELETE'])
def eliminarAsesoria(request):
    # Obtener los datos de la peticion
    idAsesoria = request.data.get('id_asesoria')
    token = request.data.get('token')

    valido, mensaje, tipo = verificarToken(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)

    try:
        asesoria_eliminar = Asesoria.objects.get(id_asesoria=idAsesoria)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'La asesoria que desea eliminar no existe', "error": False}, status=200) 

    fecha = asesoria_eliminar.fecha
    if(tipo == 'usuario'):
        usuario = Usuario.objects.get(id_usuario=asesoria_eliminar.idusuario.id_usuario)
        enviarCorreo('Hola, el usuario ' + usuario.nombre + ' ha eliminado la asesoria del dia '+ obtenerDia(fecha.day) ,'La asesoria se elimino', usuario.email)
    else:
        asesor = Asesor.objects.get(id_asesor=asesoria_eliminar.idasesor.id_asesor)
        enviarCorreo('Hola, el asesor ' + asesor.nombre + ' ha eliminado la asesoria del dia '+ obtenerDia(fecha.day) ,'La asesoria se elimino', asesor.email)
 
    asesoria_eliminar.delete()
    

    return Response({'mensaje': 'Eliminado correctamente', "error": False}, status=200) 

@api_view(['POST'])
def obtenerHorariosByAsesor(request):
    dia = request.data.get('dia')
    token = request.data.get('token')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=200)
    
    if not es_dia_semana(dia):
             return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": False}, status=200)
        

    horarios = Diahora.objects.filter(idasesor=mensaje, dia=dia)

    serializer = DiaHoraSerializer(horarios, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)




