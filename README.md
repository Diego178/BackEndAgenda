Proyecto para la Universidad Veracruzana
Tiene el fin de ayudar a las asesoras y usuarios a agendar asesorias, tener un control y evitar problemas de transpalo

Endpoints

http://127.0.0.1:8000/api/autenticacion/ # Este es para el login

Tienes que enviar un json asi:

{
    'tipo': 'asesor', # Puede ser asesor o usuario
    'credencial': 'aors@uv.mx', # Puede ser email o matricula
    'password': '12345678' # Debe tener min 8 caracteres, max 16 caracteres
}


