from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Asesor, Datosreunionvirtual, Diahora, Asesoria, Curso
from utils.validadores import es_dia_semana, es_hora_valida, es_valido_email, es_valido_modalidad, es_valido_password
from django.core.exceptions import ObjectDoesNotExist
from servicioAgenda.authentication import verificarTokenAdmin, verificarTokenAsesor, verificarToken, verificarTokenUsuario
from django.contrib.auth.hashers import make_password
from ...serializers import AsesorSerializer, AsesorSerializerGET, CursoSerializer, DatosReunionSerializer
import re 


@api_view(['GET'])
def obtenerAsesores(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)
    valido, mensaje = verificarTokenAdmin(token)
    if not valido:
        return Response({'mensaje': mensaje, "error": True}, status=401)

    asesores = Asesor.objects.all()

    serializer = AsesorSerializer(asesores, many=True)

    return Response({'mensaje': serializer.data, "error": False}, status=200)