from DigiNote.database import db
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idEstudiante = db.Column(db.Integer, primary_key=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    FechaNacimiento = db.Column(db.Date, nullable=False)
    Correo = db.Column(db.String(100), nullable=False)
    Telefono = db.Column(db.String(20))
    Direccion = db.Column(db.Text, nullable=False)
    Observacion = db.Column(db.Text)

    matriculas = db.relationship('Matricula', backref='estudiante', cascade='all, delete-orphan')
    calificaciones_quimestre = db.relationship('CalificacionesQuimestre', backref='estudiante', cascade='all, delete-orphan')
    calificaciones_final = db.relationship('CalificacionFinal', backref='estudiante', cascade='all, delete-orphan')

class Profesor(db.Model):
    __tablename__ = 'profesor'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idProfesor = db.Column(db.Integer, primary_key=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Telefono = db.Column(db.String(20))
    Correo = db.Column(db.String(100), nullable=False)
    Especialidad = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.Text)

    asignaciones = db.relationship('AsignacionCurso', backref='profesor', cascade='all, delete-orphan')

class Administrador(db.Model):
    __tablename__ = 'administrador'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    idAdministrador = db.Column(db.Integer, primary_key=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Nombre = db.Column(db.String(100), nullable=False)
    Correo = db.Column(db.String(100), nullable=False)

class Materia(db.Model):
    __tablename__ = 'materia'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idMateria = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    Descripcion = db.Column(db.Text)

    asignaciones = db.relationship('AsignacionCurso', backref='materia', cascade='all, delete-orphan')
    calificaciones_quimestre = db.relationship('CalificacionesQuimestre', backref='materia', cascade='all, delete-orphan')
    calificaciones_final = db.relationship('CalificacionFinal', backref='materia', cascade='all, delete-orphan')

class PeriodoLectivo(db.Model):
    __tablename__ = 'periodo_lectivo'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idPeriodo = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(20), nullable=False)
    FechaInicio = db.Column(db.Date, nullable=False)
    FechaFin = db.Column(db.Date, nullable=False)
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Inactivo')

    asignaciones = db.relationship('AsignacionCurso', backref='periodo', cascade='all, delete-orphan')

class AsignacionCurso(db.Model):
    __tablename__ = 'asignacion_curso'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idAsignacion = db.Column(db.Integer, primary_key=True)
    idProfesor = db.Column(db.Integer, db.ForeignKey('profesor.idProfesor', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idMateria = db.Column(db.Integer, db.ForeignKey('materia.idMateria', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Aula = db.Column(db.String(50))
    Paralelo = db.Column(db.String(10))
    HoraEntrada = db.Column(db.Time, nullable=False)
    HoraSalida = db.Column(db.Time, nullable=False)
    idPeriodo = db.Column(db.Integer, db.ForeignKey('periodo_lectivo.idPeriodo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    matricula_asignaciones = db.relationship('MatriculaAsignacion', backref='asignacion', cascade='all, delete-orphan')
    calificaciones_quimestre = db.relationship('CalificacionesQuimestre', backref='asignacion', cascade='all, delete-orphan')
    calificaciones_final = db.relationship('CalificacionFinal', backref='asignacion', cascade='all, delete-orphan')

class Matricula(db.Model):
    __tablename__ = 'matricula'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idMatricula = db.Column(db.Integer, primary_key=True)
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    FechaMatricula = db.Column(db.Date, nullable=False)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    PromedioAnual = db.Column(db.Numeric(5, 2), default=0)

    matricula_asignaciones = db.relationship('MatriculaAsignacion', backref='matricula', cascade='all, delete-orphan')

class MatriculaAsignacion(db.Model):
    __tablename__ = 'matricula_asignacion'
    __table_args__ = (
        db.UniqueConstraint('idMatricula', 'idAsignacion'),
        {'mysql_engine': 'InnoDB'}
    )

    idMatriculaAsignacion = db.Column(db.Integer, primary_key=True)
    idMatricula = db.Column(db.Integer, db.ForeignKey('matricula.idMatricula', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idAsignacion = db.Column(db.Integer, db.ForeignKey('asignacion_curso.idAsignacion', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

class CalificacionesQuimestre(db.Model):
    __tablename__ = 'calificacion_quimestre'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idQuimestre = db.Column(db.Integer, primary_key=True)
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idMateria = db.Column(db.Integer, db.ForeignKey('materia.idMateria', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idAsignacion = db.Column(db.Integer, db.ForeignKey('asignacion_curso.idAsignacion', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Quimestre = db.Column(db.Enum('1', '2'), nullable=False)
    NotaAutonoma = db.Column(db.Numeric(5, 2), default=0)
    NotaPractica = db.Column(db.Numeric(5, 2), default=0)
    NotaLeccion = db.Column(db.Numeric(5, 2), default=0)
    NotaExamen = db.Column(db.Numeric(5, 2), default=0)
    PromedioQuimestre = db.Column(db.Numeric(5, 2), default=0)

class CalificacionFinal(db.Model):
    __tablename__ = 'calificacion_final'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idCalificacionFinal = db.Column(db.Integer, primary_key=True)
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idMateria = db.Column(db.Integer, db.ForeignKey('materia.idMateria', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idAsignacion = db.Column(db.Integer, db.ForeignKey('asignacion_curso.idAsignacion', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    PromQuimestre1 = db.Column(db.Numeric(5, 2), default=0)
    PromQuimestre2 = db.Column(db.Numeric(5, 2), default=0)
    PromedioFinal = db.Column(db.Numeric(5, 2), default=0)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    idUsuario = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Rol = db.Column(db.Enum('Admin', 'Profesor', 'Estudiante'), nullable=False)
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    idProfesor = db.Column(db.Integer, db.ForeignKey('profesor.idProfesor', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    idAdministrador = db.Column(db.Integer, db.ForeignKey('administrador.idAdministrador', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)

    estudiante = db.relationship('Estudiante', backref='usuario', uselist=False)
    profesor = db.relationship('Profesor', backref='usuario', uselist=False)
    administrador = db.relationship('Administrador', backref='usuario', uselist=False)
