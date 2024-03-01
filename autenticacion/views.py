from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def loginUsuario(request):
    matricula = request.data.get('matricula')
    password = request.data.get('password')
    return Response('okay')

@api_view(['GET'])
def prueba(request):
    return Response('Correcto')