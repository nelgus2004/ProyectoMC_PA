from flask import render_template, make_response, request, Blueprint, send_file, flash, current_app

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io
import os

report_bp = Blueprint('reportes',__name__, template_folder='DigiNote/templates')


@report_bp.route('/generar_pdf', methods=['POST', 'GET'])
def generar_pdf_route():
    tipo = request.args.get('tipo', 'all')
    nivel = request.args.get('nivel', 'all')
    paralelo = request.args.get('paralelo', 'all')

    filtros = {}
    if nivel != 'all':
        filtros['nivel'] = nivel
    if paralelo != 'all':
        filtros['paralelo'] = paralelo
        
    pdf_response = generar_pdf(tipo, filtros)
    
    if isinstance(pdf_response, list) and not pdf_response:
        flash('No se pudo generar el reporte. No hay registros de la consulta.', 'warning')
        return render_template('inicio.html')

    return pdf_response


def generar_pdf(tipo, filtros):
    if tipo not in ['matricula', 'calificaciones']:
        flash('Tipo de reporte inválido', 'danger')
        return []
    
    # Crear buffer para el PDF
    buffer = io.BytesIO()
    size = A4 if tipo == 'matricula' else landscape(A4)
    doc = SimpleDocTemplate(buffer, pagesize=size, rightMargin=40, leftMargin=40, topMargin=80, bottomMargin=60)
    styles = getSampleStyleSheet()
    elementos = []

    estilo_info = styles['Normal']
    estilo_info.spaceBefore = 12
    estilo_info.spaceAfter = 12
    estilo_info.leftIndent = 20


    # Cuerpo del documento según tipo
    if tipo == 'matricula':
        datos = obtener_matriculas(filtros)
        if not datos:
            flash('No se encontraron matrículas con los filtros proporcionados', 'info')
            return []
        

        for i, estudiante in enumerate(datos):
            elementos.append(Spacer(1, 24))
            info = f"""
                <b>Estudiante:</b> {estudiante['estudiante']}<br/>
                <b>Cédula:</b> {estudiante['cedula']}<br/>
                <b>Nivel:</b> {estudiante['nivel']}<br/>
                <b>Paralelo:</b> {estudiante['paralelo']}<br/>
                <b>Periodo:</b> {estudiante['periodo']} ({estudiante['duracion_periodo']})<br/>
                <b>Fecha Matrícula:</b> {estudiante['fecha_matricula']}<br/>
            """
            elementos.append(Paragraph(info, styles['Normal']))
            elementos.append(Spacer(1, 24))
            elementos += generar_tabla_asignaciones_matricula(estudiante['asignaciones'], styles)
            
            elementos.append(Spacer(1, 34))
            nota_paragraph = Paragraph(f"<b>Nota Anual:</b> {estudiante['promedio_anual']:.2f}", styles['Normal'])
            nota_table = Table([[nota_paragraph]], colWidths=[400])
            nota_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT')])
            elementos.append(nota_table)

            if i < len(datos) - 1:
                elementos.append(PageBreak())


    elif tipo == 'calificaciones':
        datos = obtener_calificaciones(filtros)
        if not isinstance(datos, list):
            flash('No se encontraron calificaciones con los filtros proporcionados', 'info')
            return []

        for i, estudiante in enumerate(datos):
            elementos.append(Spacer(1, 24))
            info = f"""
                <b>Estudiante:</b> {estudiante['apellido']} {estudiante['nombre']} <br/>
                <b>Cédula:</b> {estudiante['cedula']}<br/>
                <b>Nivel:</b> {estudiante['nivel']}<br/>
                <b>Paralelo:</b> {estudiante['paralelo']}<br/>
            """
            elementos.append(Paragraph(info, styles['Normal']))
            elementos.append(Spacer(1, 18))
            elementos += generar_tabla_calificaciones_por_estudiante(estudiante, styles)
            elementos.append(Spacer(1, 36))
            
            if i < len(datos) - 1:
                elementos.append(PageBreak())

    doc.build(elementos, onFirstPage=encabezado_y_footer, onLaterPages=encabezado_y_footer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=False, download_name=f"{tipo}_reporte.pdf", mimetype='application/pdf')

def encabezado_y_footer(canvas, doc):
    agregar_encabezado(canvas, doc)
    agregar_footer(canvas, doc)

def agregar_encabezado(canvas, doc):
    canvas.saveState()
    
    try:
        logo_path = os.path.join(current_app.root_path, 'static', 'image', 'logo64px.png')
        canvas.drawImage(
            logo_path,
            x=doc.pagesize[0] - 60,
            y=doc.pagesize[1] - 80,
            width=40,
            height=40,
            preserveAspectRatio=True,
            mask='auto'
        )
    except Exception as e:
        print(f"Error al cargar logo: {e}")

    canvas.setFont('Helvetica-Bold', 14)
    titulo = current_app.config.get('TIPO_REPORTE', 'Reporte')
    canvas.drawCentredString(doc.pagesize[0] / 2, doc.pagesize[1] - 90, "DigiNote - Reporte")

    canvas.setStrokeColor(colors.lightgrey)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, doc.pagesize[1] - 100, doc.pagesize[0] - doc.rightMargin, doc.pagesize[1] - 100)

    canvas.restoreState()
    
    
def agregar_footer(canvas, doc):
    canvas.saveState()

    # Fecha
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
    canvas.setFont('Helvetica', 8)
    canvas.drawString(doc.leftMargin, 30, f"Generado el: {fecha}")

    # Número de página
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 30, f"Página {doc.page}")

    canvas.restoreState()
    

def generar_tabla_asignaciones_matricula(asignaciones, styles):
    elementos = []
    encabezado = ['DOCENTE', 'MATERIA', 'NIVEL', 'PARALELO', 'NOTA FINAL']
    tabla_data = [encabezado]

    for asign in asignaciones:
        fila = [
            asign['profesor'],
            asign['materia'],
            asign['nivel'],
            asign['paralelo'],
            f"{asign['promedio_final']:.2f}"
        ]
        tabla_data.append(fila)

    tabla = Table(tabla_data, hAlign='CENTER', repeatRows=1, colWidths=[140, 120, 60, 60, 70])
    tabla.setStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    elementos.append(tabla)
    return elementos


def generar_tabla_calificaciones_por_estudiante(datos, styles):
    elementos = []
    encabezado = [
        'MATERIA', 'DOCENTE',
        'Aut. Q1', 'Prác. Q1', 'Lecc. Q1', 'Exam. Q1', 'Prom. Q1',
        'Aut. Q2', 'Prác. Q2', 'Lecc. Q2', 'Exam. Q2', 'Prom. Q2',
        'Final'
    ]

    tabla_data = [encabezado]
    for materia in datos['materias']:
        fila = [
            materia['materia'],
            materia['profesor'],
            materia['notas']['primer_quimestre']['autonoma'],
            materia['notas']['primer_quimestre']['practica'],
            materia['notas']['primer_quimestre']['leccion'],
            materia['notas']['primer_quimestre']['examen'],
            materia['notas']['primer_quimestre']['promedio'],
            materia['notas']['segundo_quimestre']['autonoma'],
            materia['notas']['segundo_quimestre']['practica'],
            materia['notas']['segundo_quimestre']['leccion'],
            materia['notas']['segundo_quimestre']['examen'],
            materia['notas']['segundo_quimestre']['promedio'],
            materia['notas']['final']
        ]
        tabla_data.append(fila)

    tabla = Table(tabla_data, hAlign='CENTER', repeatRows=1)
    tabla.setStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    elementos.append(tabla)
    return elementos


from DigiNote.database import db
from DigiNote.database.models import Matricula, MatriculaAsignacion, Estudiante, Profesor, Curso, PeriodoLectivo, AsignacionCurso, Materia, Calificacion

def obtener_matriculas(filtros=None):
    # Consulta de matrículas activas
    query_matriculas = db.session.query(
        Matricula.idMatricula,
        Estudiante.Apellido,
        Estudiante.Nombre,
        Estudiante.Cedula,
        Matricula.FechaMatricula,
        Matricula.Nivel,
        Matricula.Paralelo,
        Matricula.PromedioAnual,
        PeriodoLectivo.Nombre.label('Periodo'),
        db.func.concat(
            db.func.date_format(PeriodoLectivo.FechaInicio, '%M'), '-',
            db.func.date_format(PeriodoLectivo.FechaFin, '%M')
        ).label('DuracionPeriodo')
    ).join(Estudiante, Estudiante.idEstudiante == Matricula.idEstudiante) \
     .join(PeriodoLectivo, PeriodoLectivo.idPeriodo == Matricula.idPeriodo) \
     .filter(PeriodoLectivo.Estado == 'Activo')
     
    if filtros:
        if 'nivel' in filtros:
            query_matriculas = query_matriculas.filter(Matricula.Nivel == filtros['nivel'])
        if 'paralelo' in filtros:
            query_matriculas = query_matriculas.filter(Matricula.Paralelo == filtros['paralelo'])
    matriculas = query_matriculas.all()

    # Consulta de asignaciones con calificación final
    asignaciones = db.session.query(
        MatriculaAsignacion.idMatricula,
        Materia.Nombre.label('materia'),
        Curso.Paralelo,
        Curso.Nivel,
        Profesor.Apellido.label('profesor_apellido'),
        Profesor.Nombre.label('profesor_nombre'),
        Calificacion.PromedioFinal
    ).join(AsignacionCurso, AsignacionCurso.idCursoAsignacion == MatriculaAsignacion.idCursoAsignacion) \
     .join(Materia, Materia.idMateria == AsignacionCurso.idMateria) \
     .join(Profesor, Profesor.idProfesor == AsignacionCurso.idProfesor) \
     .join(Curso, Curso.idCurso == AsignacionCurso.idCurso) \
     .join(PeriodoLectivo, PeriodoLectivo.idPeriodo == AsignacionCurso.idPeriodo) \
     .join(Calificacion, Calificacion.idMatriculaAsignacion == MatriculaAsignacion.idMatriculaAsignacion) \
     .filter(PeriodoLectivo.Estado == 'Activo') \
     .all()

    # Indexar asignaciones por idMatricula
    asignaciones_dict = {}
    for asign in asignaciones:
        if asign.idMatricula not in asignaciones_dict:
            asignaciones_dict[asign.idMatricula] = []
        asignaciones_dict[asign.idMatricula].append({
            'materia': asign.materia,
            'nivel': asign.Nivel,
            'paralelo': asign.Paralelo,
            'profesor': f"{asign.profesor_nombre} {asign.profesor_apellido}",
            'promedio_final': float(asign.PromedioFinal) if asign.PromedioFinal is not None else 0.0
        })

    # Unir matrículas con sus asignaciones
    resultado = []
    for mat in matriculas:
        matricula = {
            'idMatricula': mat.idMatricula,
            'cedula': mat.Cedula,
            'estudiante': f"{mat.Apellido} {mat.Nombre}",
            'fecha_matricula': mat.FechaMatricula.strftime('%Y-%m-%d'),
            'nivel': mat.Nivel,
            'paralelo': mat.Paralelo,
            'periodo': mat.Periodo,
            'duracion_periodo': mat.DuracionPeriodo,
            'promedio_anual': float(mat.PromedioAnual) if mat.PromedioAnual else 0.0,
            'asignaciones': asignaciones_dict.get(mat.idMatricula, [])
        }
        resultado.append(matricula)
        
    #print(f'resultado matriculas: {resultado}')
    return resultado


def obtener_calificaciones(filtros=None):
    query_matricula = db.session.query(Matricula) \
        .join(PeriodoLectivo) \
        .order_by(Matricula.FechaMatricula.desc(), Matricula.Nivel, Matricula.Paralelo)
    
    print(filtros)
    if filtros:       
        if 'nivel' in filtros:
            query_matricula = query_matricula.filter(Matricula.Nivel == filtros['nivel'])
        if 'paralelo' in filtros:
            query_matricula = query_matricula.filter(Matricula.Paralelo == filtros['paralelo'])
        
        print(str(query_matricula.statement))
        matriculas = query_matricula.all()
    else:
        print(str(query_matricula.statement))
        matriculas = query_matricula.all()


    if not matriculas:
        flash('No hay matrículas registradas con los filtros proporcionados', 'danger')
        return []

    resultados = []

    for matricula in matriculas:
        estudiante = matricula.estudiante

        calificaciones = db.session.query(
            Materia.Nombre.label('materia'),
            Profesor.Nombre.label('profesor_nombre'),
            Profesor.Apellido.label('profesor_apellido'),
            Calificacion
        ).select_from(MatriculaAsignacion) \
         .join(AsignacionCurso, AsignacionCurso.idCursoAsignacion == MatriculaAsignacion.idCursoAsignacion) \
         .join(Materia, Materia.idMateria == AsignacionCurso.idMateria) \
         .join(Profesor, Profesor.idProfesor == AsignacionCurso.idProfesor) \
         .outerjoin(Calificacion, Calificacion.idMatriculaAsignacion == MatriculaAsignacion.idMatriculaAsignacion) \
         .filter(MatriculaAsignacion.idMatricula == matricula.idMatricula) \
         .all()

        resultado = {
            'idEstudiante': estudiante.idEstudiante,
            'cedula': estudiante.Cedula,
            'nombre': estudiante.Nombre,
            'apellido': estudiante.Apellido,
            'fecha_nacimiento': estudiante.FechaNacimiento.strftime('%Y-%m-%d'),
            'telefono': estudiante.Telefono,
            'direccion': estudiante.Direccion,
            'observacion': estudiante.Observacion,
            'nivel': matricula.Nivel,
            'paralelo': matricula.Paralelo,
            'fecha_matricula': matricula.FechaMatricula.strftime('%Y-%m-%d'),
            'materias': []
        }

        for materia, profesor_nombre, profesor_apellido, calificacion in calificaciones:
            if calificacion:
                resultado['materias'].append({
                    'idCalificacion': calificacion.idCalificacion,
                    'idMatriculaAsignacion': calificacion.idMatriculaAsignacion,
                    'materia': materia,
                    'profesor': f'{profesor_nombre} {profesor_apellido}',
                    'notas': {
                        'primer_quimestre': {
                            'autonoma': float(calificacion.NotaAutonoma1),
                            'practica': float(calificacion.NotaPractica1),
                            'leccion': float(calificacion.NotaLeccion1),
                            'examen': float(calificacion.NotaExamen1),
                            'promedio': float(calificacion.PromQuimestre1)
                        },
                        'segundo_quimestre': {
                            'autonoma': float(calificacion.NotaAutonoma2),
                            'practica': float(calificacion.NotaPractica2),
                            'leccion': float(calificacion.NotaLeccion2),
                            'examen': float(calificacion.NotaExamen2),
                            'promedio': float(calificacion.PromQuimestre2)
                        },
                        'final': float(calificacion.PromedioFinal)
                    }
                })
            else:
                resultado['materias'].append({
                    'materia': materia,
                    'profesor': f'{profesor_nombre} {profesor_apellido}',
                    'notas': 'Sin calificación registrada'
                })

        resultados.append(resultado)

    return resultados


def obtener_matricula_individual(estudiante_id):
    pass

def obtener_calificaciones_individual(estudiante_matricula):
    pass

