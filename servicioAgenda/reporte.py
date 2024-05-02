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


# Extraer los datos de la base de datos
asesorias = Asesoria.objects.all().select_related('idasesor', 'idusuario', 'iddiahora', 'idcurso')

# Agrupar los datos por mes
asesorias_por_mes = asesorias.annotate(month=TruncMonth('fecha')).values('month', 'id_asesoria', 'tipo', 'tema', 'fecha', 'idasesor__nombre', 'idusuario__nombre', 'idusuario__matricula', 'iddiahora__hora_inicio', 'iddiahora__hora_termino', 'iddiahora__modalidad', 'idcurso__nombrecurso').annotate(count=Count('id_asesoria'))


def export_to_pdf(data):
    c = canvas.Canvas("reporte.pdf", pagesize=landscape(letter))
    width, height = landscape(letter)

    # Define el espacio entre las líneas y la posición inicial
    line_height = 12
    y = height - 50

    # Añade un título
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, y, "Reporte")
    y -= 30

    # Cambia el tamaño de la fuente para los encabezados de las columnas
    c.setFont("Helvetica-Bold", 14)

    # Escribe los encabezados de las columnas
    for i, column in enumerate(data[0].keys()):
        c.drawString(30 + i*100, y, str(column))

    # Cambia el tamaño de la fuente para los datos
    c.setFont("Helvetica", 10)

    # Escribe los datos
    for row in data:
        y -= line_height

        # Comprueba si necesitamos comenzar una nueva página
        if y < 50:
            c.showPage()
            y = height - 50

        for i, item in enumerate(row.values()):
            c.drawString(30 + i*100, y, str(item))

    c.save()

# Llama a la función para generar el archivo PDF
export_to_pdf(asesorias_por_mes)


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Call the function to generate the CSV file
export_to_csv(asesorias_por_mes, 'report.csv')


def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Call the function to generate the Excel file
export_to_excel(asesorias_por_mes, 'report.xlsx')


class ReporteView(APIView):
    def post(self, request, format=None):
        tipo = request.data.get('tipo')

        if tipo == 'pdf':
            filename = 'reporte.pdf'
            export_to_pdf(asesorias_por_mes)
        elif tipo == 'csv':
            filename = 'reporte.csv'
            export_to_csv(asesorias_por_mes, filename)
        elif tipo == 'xlsx':
            filename = 'reporte.xlsx'
            export_to_excel(asesorias_por_mes, filename)
        else:
            return Response({'error': 'Tipo de archivo no soportado'}, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(open(filename, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
