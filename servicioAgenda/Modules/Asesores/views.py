from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Asesor, Datosreunionvirtual, Diahora, Asesoria, Curso, Idioma
from utils.validadores import es_dia_semana, es_hora_valida, es_valido_email, es_valido_modalidad, es_valido_password
from django.core.exceptions import ObjectDoesNotExist
from servicioAgenda.authentication import verificarTokenAsesor, verificarToken, verificarTokenUsuario
from django.contrib.auth.hashers import make_password
from ...serializers import AsesorSerializer, AsesorSerializerGET, CursoSerializer, DatosReunionSerializer
import re 
import base64

@api_view(['POST'])
def registrarAsesor(request):
    # Obtener los datos de la peticion
    nombre = request.data.get('nombre')
    idioma = request.data.get('idioma')
    email = request.data.get('email')
    password = request.data.get('password')
    fotoBase64 = request.data.get('fotoBase64')

    if nombre is not None and idioma is not None and password is not None and email is not None:

        if not es_valido_email(email):
            return Response({'mensaje': 'Correo ingresado no valido', "error": True}, status=200)
        
        if not es_valido_password(password):
            return Response({'mensaje': 'La contrasena no cumple los requisitos para que sea valida', "error": True}, status=200)

        if Asesor.objects.filter(email=email).exists():
            return Response({'mensaje': 'Ya existe un asesor con este correo electrónico', "error": True}, status=200)
        
        password_encriptada = make_password(password)
        
        nuevo_asesor = Asesor(nombre=nombre, idioma=idioma, email=email, password=password_encriptada, fotoBase64=fotoBase64)

        nuevo_asesor.save()
   
        return Response({'mensaje': 'El asesor fue registrado correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)  


@api_view(['POST'])
def registrarDatosReunionVirtual(request):

    url = request.data.get('url')
    password = request.data.get('password')
    id_reunion = request.data.get('id_reunion')
    token = request.META.get('HTTP_AUTHORIZATION')


    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if url is not None and id_reunion is not None and password is not None:
        regexURL = r'^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$'

        if not re.match(regexURL, url):
            return Response({'mensaje': 'El enlace para la reunion virtual no es valido', "error": True}, status=200)
        
        if Datosreunionvirtual.objects.filter(idasesor=mensaje).exists():
            return Response({'mensaje': 'Error el asesor ya cuenta con datos para su reunion virtual.', "error": True}, status=200)
        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
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
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if dia is not None and hora_inicio is not None and hora_termino is not None and modalidad is not None:
        
        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        

        if not es_dia_semana(dia):
             return Response({'mensaje': 'Error, el dia se la semana no es valido.', "error": True}, status=200)
        
        if not es_hora_valida(hora_inicio):
             return Response({'mensaje': 'Error, la hora de inicio no es valida.', "error": True}, status=200)
        
        if not es_hora_valida(hora_termino):
             return Response({'mensaje': 'Error, la hora de termino no es valida.', "error": True}, status=200)
            
        nuevo_datos = Diahora(dia=dia, hora_inicio=hora_inicio, hora_termino=hora_termino, modalidad=modalidad, idasesor=asesor, eslibre=1, estado="activo")

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos de la reunion fueron registrados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)
    
    
@api_view(['PUT'])
def actuaizarHoraDia(request):
    id_dia_hora = request.data.get('idDiaHora')
    hora_inicio = request.data.get('hora_inicio')
    hora_termino = request.data.get('hora_termino')
    modalidad = request.data.get('modalidad')
    estado = request.data.get('estado')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if id_dia_hora is not None and hora_inicio is not None and hora_termino is not None and modalidad is not None and estado is not None:
        
        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        
        if not es_hora_valida(hora_inicio):
             return Response({'mensaje': 'Error, la hora de inicio no es valida.', "error": False}, status=200)
        
        if not es_hora_valida(hora_termino):
             return Response({'mensaje': 'Error, la hora de termino no es valida.', "error": False}, status=200)
            
        if not es_valido_modalidad(modalidad):
             return Response({'mensaje': 'Error, la modalidad no es valida.', "error": False}, status=200)
        
        try:
            # Recuperar el objeto Diahora existente
            dia_hora_existente = Diahora.objects.get(id_diahora=id_dia_hora)
        except Diahora.DoesNotExist:
            return Response({'mensaje': 'Error, el Diahora no existe en la base de datos.', "error": True}, status=200)

        if dia_hora_existente.eslibre == 0:
            return Response({'mensaje': 'No se puede guardar la informacion ya que la hora no se encuentra libre, si desea cambiar la informacion elimine la asesoria antes', "error": True}, status=200)
        
        nuevo_datos = Diahora(id_diahora=id_dia_hora, hora_inicio=hora_inicio, hora_termino=hora_termino, eslibre=dia_hora_existente.eslibre, dia=dia_hora_existente.dia, modalidad=modalidad, idasesor=asesor, estado=estado)

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos del horario fueron actualizados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)


@api_view(['DELETE'])
def eliminarHoraDia(request):
    id_dia_hora = request.data.get('id_diahora')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if id_dia_hora is not None :
        try:
            diaHora_eliminar = Diahora.objects.get(id_diahora=id_dia_hora)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, no se encontro en la base de datos', "error": True}, status=200)
        


        asesoria = Asesoria.objects.filter(iddiahora=id_dia_hora)

        if asesoria.count() > 0:
             return Response({'mensaje': 'Error, no se puede eliminar, ya que esta hora esta vinculada a una asesoria activa, por favor eliminala antes.', "error": True}, status=200)

        diaHora_eliminar.delete()
        return Response({'mensaje': 'El dia y hora de la reunion fue eliminada correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)

@api_view(['POST'])
def obtenerDatosAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesor = Asesor.objects.get(id_asesor=mensaje)
    
    # Decodificar fotoBase64 a una cadena de texto antes de enviarla
    asesor.fotoBase64 = asesor.fotoBase64.decode('utf-8')

    serializer = AsesorSerializer(asesor)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['PUT'])
def actualizarAsesor(request):
    nombre = request.data.get('nombre')
    idioma = request.data.get('idioma')
    email = request.data.get('email')
    fotoBase64 = request.data.get('fotoBase64')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if nombre is not None and email is not None and idioma is not None:

        if not es_valido_email(email):
            return Response({'mensaje': 'Correo ingresado no valido.', "error": True}, status=200)

        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        

        asesor.nombre = nombre
        asesor.idioma = idioma
        asesor.email = email
        asesor.fotoBase64 = fotoBase64  # Asignar fotoBase64 directamente
     
        asesor.save()
   
        return Response({'mensaje': 'Los datos del usuario fueron actualizados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)

@api_view(['POST'])
def obtenerCursosAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesor = Asesor.objects.get(id_asesor=mensaje)

    cursos = Curso.objects.filter(idasesor=asesor)

    serializer = CursoSerializer(cursos, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)



@api_view(['POST'])
def registrarCurso(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    nombre = request.data.get('nombre')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    if nombre is not None:

        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, el asesor no existe en la base de datos.', "error": True}, status=200)
        

        nuevo_datos = Curso(nombrecurso=nombre, idasesor=asesor)

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos del curso fueron registrados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)


@api_view(['DELETE'])
def eliminarCurso(request):
    idCurso = request.data.get('idCurso')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if idCurso is not None :
        try:
            curso = Curso.objects.get(id_curso=idCurso)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, no se encontro en la base de datos', "error": True}, status=200)

        asesoria = Asesoria.objects.filter(idcurso=curso)

        if asesoria.count() > 0:
             return Response({'mensaje': 'Error, no se puede eliminar, ya que hay cursos vinculados a una asesoria activa, por favor eliminala antes.', "error": True}, status=200)

        curso.delete()
        return Response({'mensaje': 'El curso fue eliminado correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)



@api_view(['GET'])
def obtenerAsesores(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenUsuario(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    if Idioma.objects.filter(id_usuario=mensaje).exists():
        idiomas_qs = Idioma.objects.filter(id_usuario=mensaje)
        
        idiomas = idiomas_qs.values_list('idioma', flat=True)
        print(idiomas)
        asesores = Asesor.objects.filter(idioma__in=idiomas)
        print(asesores)
        serializer = AsesorSerializerGET(asesores, many=True)
        print(serializer)
        return Response({'mensaje': serializer.data, "error": False}, status=200)
    else:
        return Response(status=204)

@api_view(['GET'])
def obtenerAsesoresAdmin(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    asesores = Asesor.objects.all()

    serializer = AsesorSerializer(asesores, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)


@api_view(['DELETE'])
def eliminarAsesor(request):
    idAsesor = request.data.get('idAsesor')

    if idAsesor is not None :

        try:
            asesor_aliminar = Asesor.objects.get(id_asesor=idAsesor)
        except ObjectDoesNotExist:
            return Response({'mensaje': 'Error, no se encontro al asesor en la base de datos', "error": True}, status=200)

        asesorias = Asesoria.objects.filter(idasesor=asesor_aliminar)

        if asesorias.count() > 0:
             return Response({'mensaje': 'Error, no se puede eliminar, ya que hay asesorias vinculadas al asesor, por favor de eliminalas antes.', "error": True}, status=200)

        cursos = Curso.objects.filter(idasesor=asesor_aliminar)

        if cursos.count() > 0:
             return Response({'mensaje': 'Error, no se puede eliminar, ya que hay cursos vinculados al asesor, por favor de eliminalos antes.', "error": True}, status=200)


        asesor_aliminar.delete()
        return Response({'mensaje': 'El asesor fue eliminado correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)



@api_view(['POST'])
def actualizarAsesorCRUD(request):
    # Obtener los datos de la peticion
    nombre = request.data.get('nombre')
    idAsesor = request.data.get('idAsesor')
    idioma = request.data.get('idioma')
    email = request.data.get('email')
    password = request.data.get('password')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    if nombre is not None and idioma is not None and password is not None and email is not None:

        if not es_valido_email(email):
            return Response({'mensaje': 'Correo ingresado no valido', "error": True}, status=200)
        
        if not es_valido_password(password):
            return Response({'mensaje': 'La contrasena no cumple los requisitos para que sea valida', "error": True}, status=200)

        nuevo_asesor = Asesor(id_asesor=idAsesor, nombre=nombre, idioma=idioma, email=email, password=password)

        nuevo_asesor.save()
   
        return Response({'mensaje': 'Datos del asesor actualizados correctamente', "error": False}, status=200)  
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)  


@api_view(['POST'])
def obtenerDatosReunionAsesoria(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    try:
        asesor = Asesor.objects.get(id_asesor=mensaje)
    except Asesor.DoesNotExist:
        return Response({'mensaje': 'No se encontró el asesor asociado al token', 'error': True}, status=404)

    # Obtener los datos de la reunión virtual del asesor
    try:
        datos_reunion = Datosreunionvirtual.objects.get(idasesor=asesor)
    except Datosreunionvirtual.DoesNotExist:
        return Response({'mensaje': 'No se encontraron datos de reunión para el asesor', 'error': True}, status=404)


    serializer = DatosReunionSerializer(datos_reunion)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['PUT'])
def actualizarDatosReunionAsesoria(request):
    id_reunion = request.data.get('id_reunion')
    url = request.data.get('url')
    password = request.data.get('password')
    id_datosreunion = request.data.get('id_datosreunion')
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)


    if id_reunion is not None and password is not None and url is not None and id_datosreunion is not None:

        try:
            asesor = Asesor.objects.get(id_asesor=mensaje)
        except Asesor.DoesNotExist:
            return Response({'mensaje': 'No se encontró el asesor asociado al token', 'error': True}, status=404)


        nuevo_datos = Datosreunionvirtual(id_datosreunion=id_datosreunion, password=password, url=url, id_reunion=id_reunion, idasesor=asesor)

        nuevo_datos.save()
   
        return Response({'mensaje': 'Los datos del usuario fueron actualizados correctamente', "error": False}, status=200)

    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)

@api_view(['PUT'])
def cambiarEstadoAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    estado = request.data.get('estado')

    valido, mensaje = verificarTokenAsesor(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    if estado is not None:
        asesor = Asesor.objects.get(idasesor=mensaje)
        if estado == 0:
            if Asesoria.objects.filter(idasesor=asesor ).count() > 0:
                return Response({'mensaje': 'No se puede desactivar ', "error": True}, status=400)
            
    else:
        return Response({'mensaje': 'Bad request', "error": True}, status=400)