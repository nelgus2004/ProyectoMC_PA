from flask import render_template, make_response, request, Blueprint, send_file
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io

report_bp = Blueprint('reportes',__name__, template_folder='DigiNote/templates')

def generar_pdf(tipo, filtros=None, estudiante_id=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=70)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = "Reporte de " + (tipo.capitalize() if tipo != "estudiante" else "Estudiante")
    elementos.append(Paragraph(titulo, styles['Title']))
    elementos.append(Spacer(1, 12))

    if tipo == "matricula":
        data = obtener_datos_matricula(filtros)
        elementos.append(Paragraph("Matrículas registradas:", styles['Heading2']))
        elementos.append(Spacer(1, 12))
        elementos.append(generar_tabla(data, styles))

    elif tipo == "calificaciones":
        data = obtener_datos_calificaciones(filtros)
        elementos.append(Paragraph("Calificaciones registradas:", styles['Heading2']))
        elementos.append(Spacer(1, 12))
        elementos.append(generar_tabla(data, styles))

    elif tipo == "estudiante":
        datos_m = obtener_matricula_individual(estudiante_id)
        datos_c = obtener_calificaciones_individual(estudiante_id)
        elementos.append(Paragraph("Datos del estudiante", styles['Heading2']))
        elementos.append(generar_tabla(datos_m, styles))
        elementos.append(PageBreak())
        elementos.append(Paragraph("Calificaciones del estudiante", styles['Heading2']))
        elementos.append(generar_tabla(datos_c, styles))

    # Footer con logo y fecha
    doc.build(elementos, onLaterPages=agregar_footer, onFirstPage=agregar_footer)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{tipo}_reporte.pdf", mimetype='application/pdf')

def generar_tabla(datos, styles):
    if not datos:
        return Paragraph("No hay datos disponibles", styles['Normal'])

    tabla = Table(datos, hAlign='CENTER')
    tabla.setStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ])
    return tabla

def agregar_footer(canvas, doc):
    logo_path = 'static/image/logo64px.png'
    canvas.saveState()
    try:
        canvas.drawImage(logo_path, doc.width + doc.leftMargin - 50, 20, width=40, height=40, preserveAspectRatio=True)
    except:
        pass
    canvas.setFont('Helvetica', 8)
    canvas.drawString(doc.leftMargin, 30, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    canvas.restoreState()



from DigiNote.database.models import Matricula, Estudiante, Curso, Calificacion

def obtener_datos_matricula(filtros=None):
    query = Matricula.query.join(Estudiante).join(Curso)
    
    if filtros:
        if 'nivel' in filtros:
            query = query.filter(Matricula.nivel == filtros['nivel'])
        if 'paralelo' in filtros:
            query = query.filter(Curso.paralelo == filtros['paralelo'])

    datos = [["Estudiante", "Curso", "Nivel", "Fecha"]]
    for m in query.all():
        datos.append([
            m.estudiante.nombre_completo,
            m.curso.nombre,
            m.nivel,
            m.fecha.strftime('%Y-%m-%d')
        ])
    return datos

def obtener_matricula_individual(estudiante_id):
    estudiante = Estudiante.query.get(estudiante_id)
    if not estudiante:
        return [["Error: estudiante no encontrado"]]

    datos = [["Campo", "Valor"]]
    datos.append(["Nombre", estudiante.nombre_completo])
    datos.append(["CI", estudiante.cedula])
    datos.append(["Email", estudiante.email])
    datos.append(["Fecha nacimiento", estudiante.fecha_nacimiento.strftime('%Y-%m-%d')])
    return datos

def obtener_calificaciones_individual(estudiante_matricula):
    calificaciones = Calificacion.query.filter_by(idMatricula=estudiante_matricula).all()
    
    datos = [["Materia", "Quimestre", "Nota"]]
    for c in calificaciones:
        datos.append([
            c.asignacion.materia.nombre,
            f"Q{c.numero_quimestre}",
            round(c.promedio, 2)
        ])
    return datos

def obtener_datos_calificaciones():
    pass