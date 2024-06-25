from django.utils import timezone

def obtenerColor(esCancelada, asistio, fecha):
    print(fecha)
    hoy = timezone.localtime(timezone.now()).date()
    print('hoy:')
    print(hoy)
    if not esCancelada and hoy == fecha:
        return "grey"
    if esCancelada:
        return "red"
    if asistio and hoy >= fecha:
         return "#28B463"
    if not asistio and hoy > fecha:
        return "orange"

    if not asistio or hoy < fecha:
        return "#3498DB"
    