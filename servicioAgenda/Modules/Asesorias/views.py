from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Asesoria, Asesor, Curso, Diahora, Usuario, Datosreunionvirtual
from django.core.exceptions import ObjectDoesNotExist
from ...serializers import DiaHoraSerializer
from utils.validadores import es_dia_semana, validar_fecha
from servicioAgenda.email import enviarCorreo
from utils.validadores import validar_fecha
from servicioAgenda.authentication import verificarTokenAsesor, verificarTokenUsuario


@api_view(['POST'])
def obtenerAsesoriasAsesor(request):
    # Obtener los datos de la peticion
    token = request.data.get('token')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesorias = Asesoria.objects.filter(idasesor=mensaje)
    data = []
    for asesoria in asesorias:
        asesoria_data = {
            'id_asesoria': asesoria.id_asesoria,
            'tipo': asesoria.tipo,
            'tema': asesoria.tema,
            'nombre_usuario': asesoria.idusuario.nombre,
            'fecha': asesoria.fecha,
            'dia': asesoria.iddiahora.dia,
            'hora_inicio': asesoria.iddiahora.hora_inicio,
            'hora_termino': asesoria.iddiahora.hora_termino,
            'curso': asesoria.idcurso.nombrecurso,
            'modalidad': asesoria.iddiahora.modalidad,
            'escancelada': asesoria.escancelada
        }
        data.append(asesoria_data)

    return Response(data, status=200)



@api_view(['POST'])
def obtenerAsesoriasUsuario(request):
    # Obtener los datos de la peticion
    token = request.data.get('token')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesorias = Asesoria.objects.filter(idusuario=mensaje)
    data = []
    for asesoria in asesorias:
        if asesoria.iddiahora.modalidad == 'virtual':
            datos_reunion = Datosreunionvirtual.objects.get(idasesor=asesoria.idasesor)
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_asesor': asesoria.idasesor.nombre,
                'fecha': asesoria.fecha,
                'tema': asesoria.tema,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino,
                'password_reunion': datos_reunion.password,
                'url_reunion': datos_reunion.url,
                'id_reunion': datos_reunion.id_reunion,
                'curso': asesoria.idcurso.nombrecurso,
                'modalidad': asesoria.iddiahora.modalidad,
                'escancelada': asesoria.escancelada
            }
            data.append(asesoria_data)
        else:
            asesoria_data = {
                'id_asesoria': asesoria.id_asesoria,
                'tipo': asesoria.tipo,
                'nombre_asesor': asesoria.idasesor.nombre,
                'fecha': asesoria.fecha,
                'tema': asesoria.tema,
                'dia': asesoria.iddiahora.dia,
                'hora_inicio': asesoria.iddiahora.hora_inicio,
                'hora_termino': asesoria.iddiahora.hora_termino,
                'curso': asesoria.idcurso.nombrecurso,
                'modalidad': asesoria.iddiahora.modalidad,
                'escancelada': asesoria.escancelada
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
    idCurso = request.data.get('idCurso')
    token = request.data.get('token')


    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if tipo is not None and tema is not None and fecha is not None and idAsesor is not None and idDiaHora is not None and mensaje is not None:
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
            usuario = Usuario.objects.get(id_usuario=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el usuario no existe en la base de datos.', "error": True}, status=200)
        
        try:
            curso = Curso.objects.get(id_curso=idCurso)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el curso no existe en la base de datos.', "error": True}, status=200)
        
        
        enviarCorreo('Hola, ' + asesor.nombre + ' el usuario '+ usuario.nombre + ' ha agregado una nueva asesoria para la fecha ' +  fecha ,'Asesoria nueva', asesor.email)

        diaHora.eslibre = 0;
        diaHora.save()
        nueva_asesoria = Asesoria(tipo=tipo, tema=tema, fecha=fecha, idasesor=asesor, iddiahora= diaHora, idusuario=usuario, idcurso=curso, escancelada = 0)

        nueva_asesoria.save()
   
        return Response({'mensaje': 'La asesoria fue registrada correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 
    
@api_view(['DELETE'])
def cancelarAsesoriaUsuario(request):
    # Obtener los datos de la peticion
    idAsesoria = request.data.get('id_asesoria')
    token = request.data.get('token')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    try:
        asesoria_eliminar = Asesoria.objects.get(id_asesoria=idAsesoria)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'La asesoria que desea eliminar no existe', "error": False}, status=200) 

    fecha = asesoria_eliminar.fecha

    usuario = Usuario.objects.get(id_usuario=mensaje)

    enviarCorreo('Hola, el usuario ' + usuario.nombre + ' ha cancelado la asesoria de la fecha '+ str(fecha), 'Una asesoria se cancelo', asesoria_eliminar.idasesor.email)

    try:
        diaHora= Diahora.objects.get(id_diahora=asesoria_eliminar.iddiahora.id_diahora)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'Error, el horario elegido no existe en la base de datos.', "error": True}, status=200)
        
    diaHora.eslibre = 1;
    diaHora.save()
    asesoria_eliminar.escancelada = 1;
    asesoria_eliminar.save()
    

    return Response({'mensaje': 'Cancelada correctamente', "error": False}, status=200) 


   
@api_view(['DELETE'])
def cancelarAsesoriaAsesor(request):
    # Obtener los datos de la peticion
    idAsesoria = request.data.get('id_asesoria')
    token = request.data.get('token')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    try:
        asesoria_eliminar = Asesoria.objects.get(id_asesoria=idAsesoria)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'La asesoria que desea eliminar no existe', "error": False}, status=200) 

    fecha = asesoria_eliminar.fecha

    asesor = Asesor.objects.get(id_asesor=mensaje)

    enviarCorreo('Hola, el asesor ' + asesor.nombre + ' ha cancelado la asesoria de la fecha '+ str(fecha), 'Una asesoria se cancelo', asesoria_eliminar.idasesor.email)

    try:
        diaHora= Diahora.objects.get(id_diahora=asesoria_eliminar.iddiahora.id_diahora)
    except ObjectDoesNotExist:
        return Response({'mensaje': 'Error, el horario elegido no existe en la base de datos.', "error": True}, status=200)
        
    diaHora.eslibre = 1;
    diaHora.save()
    asesoria_eliminar.escancelada = 1;
    asesoria_eliminar.save()
    

    return Response({'mensaje': 'Cancelada correctamente', "error": False}, status=200) 


@api_view(['POST'])
def obtenerHorariosByAsesor(request):
    dia = request.data.get('dia')
    token = request.data.get('token')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    if not es_dia_semana(dia):
             return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": False}, status=200)
        

    horarios = Diahora.objects.filter(idasesor=mensaje, dia=dia)

    serializer = DiaHoraSerializer(horarios, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['POST'])
def obtenerHorariosByDia(request):
    dia = request.data.get('dia')
    modalidad = request.data.get('modalidad')
    idAsesor = request.data.get('idAsesor')
    token = request.data.get('token')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    if modalidad is not None and idAsesor is not None and dia is not None:
    
        if not es_dia_semana(dia):
                return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": False}, status=200)
        
        horarios = Diahora.objects.filter(idasesor=idAsesor, dia=dia, modalidad=modalidad, eslibre=1, estado="activo")
        
        data = []
        
        for hora in horarios:
            hora_data = {
                'idDiaHora': hora.id_diahora,
                "hora": hora.hora_inicio.strftime("%H:%M") + " a " + hora.hora_termino.strftime("%H:%M")
            }
            data.append(hora_data)

        return Response({'mensaje': data, "error": False}, status=200)
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400) 


