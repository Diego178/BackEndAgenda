from datetime import datetime, date
def obtenerColor(esCancelada, asistio, fecha):
    print(fecha)
    # hoy = datetime.now()
    
    
    # hoy = datetime.strptime(hoy, '%Y-%m-%d')
    
    # print(hoy)
    # if asistio and hoy > fecha :
    #     return "green"
        
    if esCancelada:
        return "red"
    else: 
        return "green"
    
    # if not asistio and hoy > fecha:
    #     return "blue"
    
    # if not asistio and hoy < fecha:
    #     return "orange"