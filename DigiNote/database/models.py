from DigiNote.database import db
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idEstudiante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    FechaNacimiento = db.Column(db.Date, nullable=False)
    Telefono = db.Column(db.String(20))
    Direccion = db.Column(db.Text, nullable=False)
    Observacion = db.Column(db.Text)

    matriculas = db.relationship('Matricula', back_populates='estudiante', cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', back_populates='estudiante', uselist=False)


class Profesor(db.Model):
    __tablename__ = 'profesor'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idProfesor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Telefono = db.Column(db.String(20))
    Especialidad = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.Text)

    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='profesor', cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', back_populates='profesor', uselist=False)


class Administrador(db.Model):
    __tablename__ = 'administrador'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    idAdministrador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellido = db.Column(db.String(50))

    usuario = db.relationship('Usuario', back_populates='administrador', uselist=False)


class Materia(db.Model):
    __tablename__ = 'materia'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMateria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.Text)
    
    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='materia', cascade='all, delete-orphan')


class PeriodoLectivo(db.Model):
    __tablename__ = 'periodo_lectivo'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idPeriodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(20), nullable=False)
    FechaInicio = db.Column(db.Date, nullable=False)
    FechaFin = db.Column(db.Date, nullable=False)
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Inactivo')

    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='periodo', cascade='all, delete-orphan')


class Curso(db.Model):
    __tablename__ = 'curso'
    __table_args__ = (
        db.UniqueConstraint('Nivel', 'Paralelo', name='uq_nivel_paralelo'),
        {'mysql_engine': 'InnoDB'}
    )
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idCurso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    Paralelo = db.Column(db.String(10), nullable=False)

    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='curso', cascade='all, delete-orphan')


class AsignacionCurso(db.Model):
    __tablename__ = 'asignacion_curso'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idAsignacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProfesor = db.Column(db.Integer, db.ForeignKey('profesor.idProfesor', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idMateria = db.Column(db.Integer, db.ForeignKey('materia.idMateria', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idCurso = db.Column(db.Integer, db.ForeignKey('curso.idCurso', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    Aula = db.Column(db.String(50))
    HoraEntrada = db.Column(db.Time, nullable=False)
    HoraSalida = db.Column(db.Time, nullable=False)
    idPeriodo = db.Column(db.Integer, db.ForeignKey('periodo_lectivo.idPeriodo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    matricula_asignacion = db.relationship('MatriculaAsignacion', back_populates='asignaciones_curso', cascade='all, delete-orphan')
    calificacion_final = db.relationship('CalificacionFinal', back_populates='asignaciones_curso', cascade='all, delete-orphan')
    profesor = db.relationship('Profesor', back_populates='asignaciones_curso')
    materia = db.relationship('Materia', back_populates='asignaciones_curso')
    curso = db.relationship('Curso', back_populates='asignaciones_curso')
    periodo = db.relationship('PeriodoLectivo', back_populates='asignaciones_curso')


class Matricula(db.Model):
    __tablename__ = 'matricula'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMatricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    FechaMatricula = db.Column(db.Date, nullable=False)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    Paralelo = db.Column(db.String(10), nullable=False)
    PromedioAnual = db.Column(db.Numeric(5, 2), default=0)

    estudiante = db.relationship('Estudiante', back_populates='matriculas')
    matricula_asignacion = db.relationship('MatriculaAsignacion', back_populates='matricula', cascade='all, delete-orphan')


class MatriculaAsignacion(db.Model):
    __tablename__ = 'matricula_asignacion'
    __table_args__ = (
        db.UniqueConstraint('idMatricula', 'idAsignacion', name='uq_matricula_asignacion'),
        {'mysql_engine': 'InnoDB'}
    )
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMatriculaAsignacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMatricula = db.Column(db.Integer, db.ForeignKey('matricula.idMatricula', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idAsignacion = db.Column(db.Integer, db.ForeignKey('asignacion_curso.idAsignacion', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    matricula = db.relationship('Matricula', back_populates='matricula_asignacion')
    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='matricula_asignacion')
    calificacion_final = db.relationship('CalificacionFinal', back_populates='matricula_asignacion', uselist=False)


class CalificacionesQuimestre(db.Model):
    __tablename__ = 'calificacion_quimestre'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idQuimestre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCalificacionFinal = db.Column(
        db.Integer,
        db.ForeignKey('calificacion_final.idCalificacionFinal', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    Quimestre = db.Column(db.Enum('1', '2'), nullable=False)
    NotaAutonoma = db.Column(db.Numeric(5, 2), default=0)
    NotaPractica = db.Column(db.Numeric(5, 2), default=0)
    NotaLeccion = db.Column(db.Numeric(5, 2), default=0)
    NotaExamen = db.Column(db.Numeric(5, 2), default=0)
    PromedioQuimestre = db.Column(db.Numeric(5, 2), default=0)

    calificacion_final = db.relationship('CalificacionFinal', back_populates='quimestres')
    

class CalificacionFinal(db.Model):
    __tablename__ = 'calificacion_final'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    idCalificacionFinal = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMatriculaAsignacion = db.Column(
        db.Integer,
        db.ForeignKey('matricula_asignacion.idMatriculaAsignacion', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        unique=True 
    )
    idAsignacionCurso = db.Column(
        db.Integer, 
        db.ForeignKey('asignacion_curso.idAsignacion', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    PromQuimestre1 = db.Column(db.Numeric(5, 2), default=0)
    PromQuimestre2 = db.Column(db.Numeric(5, 2), default=0)
    PromedioFinal = db.Column(db.Numeric(5, 2), default=0)

    matricula_asignacion = db.relationship('MatriculaAsignacion', back_populates='calificacion_final')
    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='calificacion_final')
    quimestres = db.relationship('CalificacionesQuimestre', back_populates='calificacion_final', cascade='all, delete-orphan')


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Correo = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Rol = db.Column(db.Enum('Admin', 'Profesor', 'Estudiante', 'Invitado'), nullable=False)
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    idProfesor = db.Column(db.Integer, db.ForeignKey('profesor.idProfesor', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    idAdministrador = db.Column(db.Integer, db.ForeignKey('administrador.idAdministrador', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)

    estudiante = db.relationship('Estudiante', back_populates='usuario', uselist=False)
    profesor = db.relationship('Profesor', back_populates='usuario', uselist=False)
    administrador = db.relationship('Administrador', back_populates='usuario', uselist=False)
