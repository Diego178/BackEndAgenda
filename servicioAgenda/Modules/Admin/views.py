from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Asesor
from servicioAgenda.authentication import verificarTokenAdmin
from ...serializers import AsesorSerializer, AsesorSerializerGETAdmin
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def obtenerAsesores(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    asesores = Asesor.objects.all()

    serializer = AsesorSerializerGETAdmin(asesores, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)

@api_view(['PATCH'])
def actualizarAsesor(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    id_asesor = request.data.get('id_asesor')
    
    print(token)
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
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)