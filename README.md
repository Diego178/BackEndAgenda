Proyecto para la Universidad Veracruzana
Tiene el fin de ayudar a las asesoras y usuarios a agendar asesorias, tener un control y evitar problemas de transpalo

Endpoints

@POST
http://127.0.0.1:8000/api/autenticacion/ # Este es para el login

Tienes que enviar un json asi:

{
    'tipo': 'asesor', # Puede ser asesor o usuario
    'credencial': 'aors@uv.mx', # Puede ser email o matricula
    'password': '12345678' # Debe tener min 8 caracteres, max 16 caracteres
}

Respuestas:
    - Error
        Los mensajes de error pueden ser por mandar datos invalidos, incompletos, o datos que no se encuentren en la base de datos, en este caso se regresara un mensaje y un valor booleano True
    - Valido
        Si se envian los datos bien regresara el asesor o usuario, con un valor booleano y el tipo de usuario registrado

http://127.0.0.1:8000/api/asesores/registrar/ # Este es para registrar un asesor

Tienes que enviar un json asi:

{
    "nombre": "Rocio",
    "email": "adors@uv.mx",
    "idioma": "frances",
    "password": "12345678"
}



http://127.0.0.1:8000/api/usuarios/registrar/ # Este es para registrar un usuario

Tienes que enviar un json asi:

{
    "nombre": "Juan Perez Rodriguez",
    "matricula": "S20018149",
    "email": "france@gmail.com",
    "password": "1234567"
}



