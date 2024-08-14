from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Admin, Asesor, Asesoria, Usuario
from servicioAgenda.authentication import verificarTokenAdmin
from ...serializers import AdminSerializer, AdminSerializerGETAdmin, AsesorSerializer, AsesorSerializerGETAdmin, UsuarioSerializer, UsuarioSerializerGETAdmin
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.hashers import make_password


@api_view(['GET'])
def obtenerAsesores(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    asesores = Asesor.objects.annotate(num_asesorias=Count('asesorias'))

    serializer = AsesorSerializerGETAdmin(asesores, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['PATCH'])
def actualizarAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    id_asesor = request.data.get('id_asesor')
    
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    asesor = get_object_or_404(Asesor, pk=id_asesor)
    
    data = {
        'nombre': request.data.get('nombre'),
        'email': request.data.get('email'),
        'idioma': request.data.get('idioma'),
        'fotoBase64': request.data.get('fotoBase64')
    }
    
    serializer = AsesorSerializer(asesor, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response( { "error": False }, status=200 )
    return Response({ "error": True }, status=400)

@api_view(['GET'])
def obtenerUsuarios(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    usuarios = Usuario.objects.all()

    serializer = UsuarioSerializerGETAdmin(usuarios, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['PATCH'])
def estadoAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    id_asesor = request.data.get('id_asesor')
    
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    if id_asesor is not None:
        asesor = get_object_or_404(Asesor, pk=id_asesor)
        
        mensaje = ''
        if asesor.activo:
            if Asesoria.objects.filter(idasesor=asesor).exists():
                return Response({'mensaje': 'No se puede desactivar la cuenta, el asesor tiene asesorias activas pendientes, por favor cancelelas primero para poder descativar la cuenta.', "error": True}, status=200)
            else:    
                asesor.activo = 0
                mensaje = 'Se desactivo la cuenta'
        else:
            asesor.activo = 1
            mensaje = 'Se activo la cuenta'
        
        asesor.save()
        return Response({'mensaje': mensaje, "error": False}, status=200)
    return Response({ "error": True }, status=400)
        

@api_view(['PATCH'])
def actualizarUsuario(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    id_usuario = request.data.get('id_usuario')
    
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    
    data = {
        'nombre': request.data.get('nombre'),
        'email': request.data.get('email'),
        'matricula': request.data.get('matricula'),
    }
    
    serializer = UsuarioSerializer(usuario, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response( { "error": False }, status=200 )
    return Response({ "error": True }, status=400)

@api_view(['GET'])
def obtenerAdmins(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    administradores = Admin.objects.all()

    serializer = AdminSerializerGETAdmin(administradores, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['POST'])
def registrarAdministrador(request):
    token = request.META.get('HTTP_AUTHORIZATION')

    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    data = {
        'nombre': request.data.get('nombre'),
        'email': request.data.get('email'),
        'password': request.data.get('password'),
    }
    if Admin.objects.filter(email=data['email']).exists():
        return Response({'mensaje': "El correo ya esta registrado en la base de datos, ingrese otro", "error": True}, status=200)
    
    if not all(data.values()):
        return Response({'mensaje': 'Datos incompletos', "error": True}, status=400)
    
    serializer = AdminSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response( { "error": False }, status=200 )
    return Response({ "error": True }, status=400)


@api_view(['PATCH'])
def actualizarAdmin(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    id = request.data.get('id')
    
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)
    
    #if id == mensaje:
     #   return Response({'mensaje': "No se puede eliminar, el administrador tiene una sesion abierta", "error": True}, status=200)
    
    admin = get_object_or_404(Admin, pk=id)
    
    data = {
        'nombre': request.data.get('nombre'),
        'email': request.data.get('email'),
    }
    
    serializer = AdminSerializer(admin, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response( { "error": False }, status=200 )
    return Response({ "error": True }, status=400)