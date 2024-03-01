from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    return Response({})

@api_view(['POST'])
def registrarse(request):
    return Response({})