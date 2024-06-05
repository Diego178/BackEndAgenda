from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Asesoria, Usuario, Asesor, Diahora, Curso
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import csv
import pandas as pd
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,LongTable
from datetime import date, timedelta
from io import BytesIO
from django.http import FileResponse
from servicioAgenda.authentication import verificarTokenAsesor


def get_joined_data():
    # Asesoria tiene relaciones ForeignKey a Usuario, Asesor, Diahora y Curso
    asesorias = Asesoria.objects.select_related('idusuario', 'idasesor', 'iddiahora', 'idcurso')

    for asesoria in asesorias:
        TodasAsesorias = {
            'id_asesoria': asesoria.id_asesoria,
            'tipo': asesoria.tipo,
            'tema': asesoria.tema,
            'fecha': asesoria.fecha,
            'escancelada': asesoria.escancelada,
            'idasesor': asesoria.idasesor.nombre if asesoria.idasesor else None,
            'idusuario': asesoria.idusuario.nombre if asesoria.idusuario else None,
            'iddiahora': asesoria.iddiahora.dia if asesoria.iddiahora else None,
            'idcurso': asesoria.idcurso.nombrecurso if asesoria.idcurso else None,
            'asistio': asesoria.asistio
        }
        yield TodasAsesorias
        
        
def get_joined_data_for_asesor(asesor_id,mes):


    primer_dia_del_mes = date(date.today().year, mes, 1)

    # Calcular la fecha del último día del mes especificado
    if mes == 12:
        ultimo_dia_del_mes = date(date.today().year + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia_del_mes= date(date.today().year, mes + 1, 1) - timedelta(days=1)
    
    
    # Asesoria tiene relaciones ForeignKey a Usuario, Asesor, Diahora y Curso
    asesorias = Asesoria.objects.filter(idasesor=asesor_id,fecha__range=(primer_dia_del_mes,ultimo_dia_del_mes)).select_related('idusuario', 'idasesor', 'iddiahora', 'idcurso')

    for asesoria in asesorias:
        if asesoria.escancelada == 0:
            fuecancelada= "No"
        else:
            fuecancelada= "Si"
        if asesoria.asistio == 0:
            asistio = "No"
        else:
            asistio = "Si"
        
        TodasAsesorias = {
            'id_asesoria': asesoria.id_asesoria,
            'tipo': asesoria.tipo,
            'tema': asesoria.tema,
            'fecha': asesoria.fecha.strftime('%d-%m-%y') if asesoria.fecha else None,
            'fue cancelada': fuecancelada,
            'Nombre asesor': asesoria.idasesor.nombre if asesoria.idasesor else None,
            'Nombre Usuario': asesoria.idusuario.nombre if asesoria.idusuario else None,
            'dia': asesoria.iddiahora.dia if asesoria.iddiahora else None,
            'hora inicio': asesoria.iddiahora.hora_inicio.strftime('%H:%M') if asesoria.iddiahora and asesoria.iddiahora.hora_inicio else None,
            'hora termino': asesoria.iddiahora.hora_termino.strftime('%H:%M') if asesoria.iddiahora and asesoria.iddiahora.hora_termino else None,
            'idcurso': asesoria.idcurso.nombrecurso if asesoria.idcurso else None,
            'asistio': asistio,
            'comentario de cancelacion': asesoria.comentario if asesoria.comentario else 'No hay comentarios'
        }
        yield TodasAsesorias



# Quiero mostrar en txt las asesorias
def export_to_txt(data, filename):
    # # Crear un objeto BytesIO
    # buffer = BytesIO()
    
    # with open(filename, 'w') as file:
    #     for asesoria in data:
    #         file.write(f'{asesoria["id_asesoria"]}, {asesoria["tipo"]}, {asesoria["tema"]}, {asesoria["fecha"]}, {asesoria["fue cancelada"]}, {asesoria["Nombre asesor"]}, {asesoria["Nombre Usuario"]}, {asesoria["dia"]}, {asesoria["hora inicio"]}, {asesoria["hora termino"]}, {asesoria["idcurso"]}, {asesoria["asistio"]}, {asesoria["comentario de cancelacion"]}\n')
            
    # # Obtener el valor del objeto BytesIO
    # txt_data = buffer.getvalue()
    
    # # Crear una respuesta con el TXT
    # response = FileResponse(BytesIO(txt_data), as_attachment=True, filename='report.txt')
    
    # return response       
    
    with open(filename, 'w') as file:
        for asesoria in data:
            file.write(f'{asesoria["id_asesoria"]}, {asesoria["tipo"]}, {asesoria["tema"]}, {asesoria["fecha"]}, {asesoria["fue cancelada"]}, {asesoria["Nombre asesor"]}, {asesoria["Nombre Usuario"]}, {asesoria["dia"]}, {asesoria["hora inicio"]}, {asesoria["hora termino"]}, {asesoria["idcurso"]}, {asesoria["asistio"]}, {asesoria["comentario de cancelacion"]}\n')
   

def export_to_pdf(data, filename,mes):
    # Crear un objeto BytesIO
    buffer = BytesIO()
    
    c = SimpleDocTemplate(filename, pagesize=landscape(letter))
    story = []
    
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    #Hacer encabezado
    #El encabezado debe llevar el Reporte de asesorias, el nombre del asesor y la fecha de creacion
    if mes == 1:
        mes_reporte = ' Enero'
    elif mes == 2:
        mes_reporte = ' Febrero'
    elif mes == 3:
        mes_reporte = ' Marzo'
    elif mes == 4:
        mes_reporte = ' Abril'
    elif mes == 5:
        mes_reporte = ' Mayo'
    elif mes == 6:
        mes_reporte = ' Junio'
    elif mes == 7:
        mes_reporte = ' Julio'
    elif mes == 8:
        mes_reporte = ' Agosto'
    elif mes == 9:
        mes_reporte = ' Septiembre'
    elif mes == 10:
        mes_reporte = ' Octubre'
    elif mes == 11:
        mes_reporte = ' Noviembre'
    elif mes == 12:
        mes_reporte = ' Diciembre'
    header = [['Reporte de asesorias'+mes_reporte, 'Nombre del asesor: '+data[0]['Nombre asesor'], "Fecha: "+d1]]
    
    #para hacer pruebas que se desborda la segunda tabla voy a agregar rows en el encabezado
    #for i in range(0, 20):
        #header.append([" ", " ", " "])
    
    # Crear la tabla
    table1 = Table(header)
    
    style1 = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 16),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND',(0,1),(-1,-1),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.white)
    ])
    
    table1.setStyle(style1)
    
    story.append(table1)
    
    # Crear las filas de la tabla
    rows = [["ID", "Tipo", "Tema", "Fecha", "Fue cancelada", "Nombre asesor", "Nombre Usuario", "Dia", "Horario", "Curso", "Asistio", "Comentario de cancelacion"]]
    for asesoria in data:
        row = [asesoria["id_asesoria"], asesoria["tipo"], asesoria["tema"], asesoria["fecha"], asesoria["fue cancelada"], asesoria["Nombre asesor"], asesoria["Nombre Usuario"], asesoria["dia"], asesoria["hora inicio"] + " - " + asesoria["hora termino"], asesoria["idcurso"], asesoria["asistio"], asesoria["comentario de cancelacion"]]
        rows.append(row)

    # Crear la tabla
    table = LongTable(rows)

    # Establecer el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.yellow),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7),

        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('BACKGROUND',(0,1),(-1,-1),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ])
    table.setStyle(style)

    # Agregar la tabla al lienzo
    story.append(table)
    c.build(story)
    
    
    # Obtener el valor del objeto BytesIO
    pdf = buffer.getvalue()

    # Crear una respuesta con el PDF
    response = FileResponse(BytesIO(pdf), as_attachment=True, filename='report.pdf')

    return response
    

def export_to_csv(data, filename):
    # Crear un objeto BytesIO
    buffer = BytesIO()

    # Escribir los datos en el objeto BytesIO
    writer = csv.DictWriter(buffer, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    # Obtener el valor del objeto BytesIO
    csv_data = buffer.getvalue()

    # Crear una respuesta con el CSV
    response = FileResponse(BytesIO(csv_data), as_attachment=True, filename='report.csv')

    return response

def export_to_excel(data, filename):
    # Crear un objeto BytesIO
    buffer = BytesIO()

    # Escribir los datos en el objeto BytesIO
    df = pd.DataFrame(data)
    df.to_excel(buffer, index=False)

    # Obtener el valor del objeto BytesIO
    excel_data = buffer.getvalue()

    # Crear una respuesta con el Excel
    response = FileResponse(BytesIO(excel_data), as_attachment=True, filename='report.xlsx')

    return response


class ReporteView(APIView):
    def post(self, request, format=None):
        tipo = request.data.get('tipo')
        token = request.META.get('HTTP_AUTHORIZATION')
        mes=request.data.get('mes')
        
        valido, mensaje = verificarTokenAsesor(token)
        if not valido:
            return Response({'mensaje': mensaje, "error": True}, status=401)
        
        idAsesor = mensaje
        
        #Quiero mostrar todos los datos asesorias
        asesorias = list(get_joined_data_for_asesor(idAsesor,mes))

        if tipo == 'pdf':
            filename = 'reporte'+mes+mensaje+'.pdf'
            return export_to_pdf(asesorias, filename)
        elif tipo == 'csv':
            filename = 'reporte'+mes+mensaje+'.pdf'
            return export_to_csv(asesorias, filename)
        elif tipo == 'xlsx':
            filename = 'reporte'+mes+mensaje+'.pdf'
            return export_to_excel(asesorias, filename)
        elif tipo == 'txt':
            filename = 'reporte'+mes+mensaje+'.pdf'
            # return export_to_txt(asesorias, filename) 
            export_to_txt(asesorias, filename)
        else:
            return Response({'error': 'Tipo de archivo no soportado'}, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(open(filename, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
