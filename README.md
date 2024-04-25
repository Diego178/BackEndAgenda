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

Respuestas:
    - Error
        Los mensajes de error pueden ser por mandar datos invalidos, incompletos, o que el email no sea valido, o que ya estuviera registrado, y por ultimo, que la contraseña no cumpla los caracteres max (16) o min (8)
    - Valido
        Si se envian los datos bien regresata error false y un mensaje satisfactorio.


http://127.0.0.1:8000/api/usuarios/registrar/ # Este es para registrar un usuario

Tienes que enviar un json asi:

{
    "nombre": "Juan Perez Rodriguez",
    "matricula": "S20018149",
    "email": "france@gmail.com",
    "password": "1234567"
}

Respuestas:
    - Error
        Los mensajes de error pueden ser por mandar datos invalidos, incompletos, o que el email no sea valido, o que ya estuviera registrado, y por ultimo, que la contraseña no cumpla los caracteres max (16) o min (8)
    - Valido
        Si se envian los datos bien regresata error false y un mensaje satisfactorio.

http://127.0.0.1:8000/api/asesores/registrarDatosReunion/

{
    "url": "https://uveracruzana.zoom.us/j/82030863166?pwd=Y3Vta0JPUnM2a1RuTEtvK1Y5SGMzUT09",
    "password": "837192",
    "id_reunion": "820 3086 3166",
    "idAsesor": 4
}

http://127.0.0.1:8000/api/asesores/registrarDiaHora/

{
  "dia": "lunes",
  "hora_inicio": "10:30:00",
  "hora_termino": "11:",
  "modalidad": "virtual",
  "idAsesor": 2
}



http://127.0.0.1:8000/api/asesorias/eliminar/ # No lleva cuerpo

http://127.0.0.1:8000/api/asesorias/obtenerAsesor/<id_asesor>/

http://127.0.0.1:8000/api/asesores/actualizarDiaHora/

{
  "idDiaHora": 1,
  "dia": "martes",
  "hora_inicio": "10:30:00",
  "hora_termino": "12:25:00",
  "modalidad": "virtual",
  "esLibre": false,
  "estado": "activo",
  "idAsesor": 2
}

http://127.0.0.1:8000/api/asesores/eliminarDiaHora/

{
    "id_diahora": 1
}

//TODO

-Editar la informacion
-registrar, editar, eliminar asesoria
-eliminar diahora

http://127.0.0.1:8000/api/asesores/obtenerDatosAsesor/

{
    "idAsesor": 1,
    "token":  "XXXXXXXXX"
}

http://127.0.0.1:8000/api/asesorias/obtenerHorariosByAsesor/

{
    "dia": "lunes",
    "token":  "XXXXXXXXX"
}


modificar agregar dia hora
ver los tokens en frontend

agregar 2 horitas



poner seguridad a todo (quitar consoleslogs, passwords encriptadas)
acabar los estilos
terminar los modales
cambiar estatico a dinamico asesores (tarea grande) (endpoint obtener asesores, y guardar imagen) (hacer crud)
hacer admin crud para asesores
filtros de card de asesoria segun la fecha
en la pantalla de registro mostrar el dia y mes que se realizara
agregar modal (aceptar cancelar) al eliminar diahora
falta refrescar asesorias al eliminar una asesoria en asesor y usuario
agregar, eliminar cursos
datos zoom



