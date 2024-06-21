from django.utils import timezone
def obtenerColor(esCancelada, asistio, fecha):
    print(fecha)
    hoy = timezone.now().date()
    if not esCancelada and hoy == fecha:
        return "grey"
    if asistio and hoy > fecha:
         return "green"
        
    if esCancelada:
        return "red"
    
    if not asistio and hoy > fecha:
        return "blue"
    
    if not asistio and hoy <= fecha:
        return "orange"