from datetime import datetime

def es_dia_semana(dia):
    dias_semana = {
        'lunes',
        'martes',
        'miércoles',
        'jueves',
        'viernes',
    }
    for string in dias_semana:
        if string == dia:
            return True
    return False
        
    
def es_hora_valida(hora):
    try:
        datetime.strptime(hora, '%H:%M:%S')
        return True
    except ValueError:
        return False
    
from datetime import datetime

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def es_valido_modalidad(modalidad):
    modalidades = {
        'virtual',
        'presencial'
    }
    for string in modalidades:
        if string == modalidad:
            return True
    return False