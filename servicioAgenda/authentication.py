import jwt
from datetime import datetime, timedelta
from utils.validadores import validar_tipo_usuario
from asesores.models import Asesor
from usuarios.models import Usuario

def crearToken(id, tipo):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.utcnow() + timedelta(minutes=120),
        'iat': datetime.utcnow(),
        'tipo': tipo
    }, 'access_secret', algorithm='HS256')


def verificarToken(token):
    try:
        # Decodificar el token
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])

        # Verificar la expiración del token
        fecha_expiracion = datetime.fromtimestamp(payload['exp'])
        if fecha_expiracion < datetime.now():
            return False, 'El token ha expirado'

        # Verificar que el user_id sea válido
        user_id = payload.get('user_id')

        tipo_usuario = payload.get('tipo')
        valido, tipo = validar_tipo_usuario(tipo_usuario)
        if valido:
            if tipo == 'asesor':
                if not Asesor.objects.filter(id_asesor=user_id).exists():
                    return False, 'No existe el usuario en la BD'
            else:
                if not Usuario.objects.filter(id_usuario=user_id).exists():
                    return False, 'No existe el usuario en la BD'
        

        # Si todas las verificaciones pasaron, el token es válido
        return True, user_id

    except jwt.ExpiredSignatureError:
        return False, 'El token ha expirado'
    except jwt.InvalidTokenError:
        return False, 'Token inválido'
    

def verificarTokenAsesor(token):
    try:
        # Decodificar el token
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])

        # Verificar la expiración del token
        fecha_expiracion = datetime.fromtimestamp(payload['exp'])
        if fecha_expiracion < datetime.now():
            return False, 'El token ha expirado'

        # Verificar que el user_id sea válido
        user_id = payload.get('user_id')

        tipo_usuario = payload.get('tipo')

        if tipo_usuario == 'asesor':
            if not Asesor.objects.filter(id_asesor=user_id).exists():
                return False, 'No existe el usuario en la BD'
        else:
            return False, 'No tienes permisos para realizar esta accion'
        

        # Si todas las verificaciones pasaron, el token es válido
        return True, user_id

    except jwt.ExpiredSignatureError:
        return False, 'El token ha expirado'
    except jwt.InvalidTokenError:
        return False, 'Token inválido'



