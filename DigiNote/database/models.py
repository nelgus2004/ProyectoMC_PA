from DigiNote.database import db
from sqlalchemy import func
from datetime import datetime

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
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

    matricula = db.relationship('Matricula', back_populates='estudiante', cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', back_populates='estudiante', uselist=False)


class Profesor(db.Model):
    __tablename__ = 'profesor'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
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
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    idAdministrador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cedula = db.Column(db.String(20), unique=True, nullable=False)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellido = db.Column(db.String(50))

    usuario = db.relationship('Usuario', back_populates='administrador', uselist=False)


class Materia(db.Model):
    __tablename__ = 'materia'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMateria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.Text)
    
    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='materia', cascade='all, delete-orphan')


class PeriodoLectivo(db.Model):
    __tablename__ = 'periodo_lectivo'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idPeriodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(20), nullable=False)
    FechaInicio = db.Column(db.Date, nullable=False)
    FechaFin = db.Column(db.Date, nullable=False)
    Estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Inactivo')

    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='periodo', cascade='all, delete-orphan')
    matriculas = db.relationship("Matricula", backref="periodo")


class Curso(db.Model):
    __tablename__ = 'curso'
    __table_args__ = (
        db.UniqueConstraint('Nivel', 'Paralelo', name='uq_nivel_paralelo'),
        {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    )
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idCurso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    Paralelo = db.Column(db.String(10), nullable=False)

    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='curso', cascade='all, delete-orphan')


class AsignacionCurso(db.Model):
    __tablename__ = 'asignacion_curso'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idCursoAsignacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProfesor = db.Column(db.Integer, db.ForeignKey('profesor.idProfesor', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idMateria = db.Column(db.Integer, db.ForeignKey('materia.idMateria', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idCurso = db.Column(db.Integer, db.ForeignKey('curso.idCurso', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    Aula = db.Column(db.String(50))
    HoraEntrada = db.Column(db.Time, nullable=False)
    HoraSalida = db.Column(db.Time, nullable=False)
    idPeriodo = db.Column(db.Integer, db.ForeignKey('periodo_lectivo.idPeriodo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    matricula_asignacion = db.relationship('MatriculaAsignacion', back_populates='asignaciones_curso', cascade='all, delete-orphan')
    profesor = db.relationship('Profesor', back_populates='asignaciones_curso')
    materia = db.relationship('Materia', back_populates='asignaciones_curso')
    curso = db.relationship('Curso', back_populates='asignaciones_curso')
    periodo = db.relationship('PeriodoLectivo', back_populates='asignaciones_curso')


class Matricula(db.Model):
    __tablename__ = 'matricula'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMatricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idEstudiante', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    FechaMatricula = db.Column(db.Date, nullable=False)
    Nivel = db.Column(db.Enum('1ro', '2do', '3ro'), nullable=False)
    Paralelo = db.Column(db.String(10), nullable=False)
    PromedioAnual = db.Column(db.Numeric(5, 2), default=0)
    idPeriodo = db.Column(db.Integer, db.ForeignKey('periodo_lectivo.idPeriodo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    estudiante = db.relationship('Estudiante', back_populates='matricula')
    matricula_asignacion = db.relationship('MatriculaAsignacion', back_populates='matricula', cascade='all, delete-orphan')
    calificaciones = db.relationship("Calificacion", backref="matricula")


class MatriculaAsignacion(db.Model):
    __tablename__ = 'matricula_asignacion'
    __table_args__ = (
        db.UniqueConstraint('idMatricula', 'idCursoAsignacion', name='uq_matricula_asignacion'),
        {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}
    )
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    idMatriculaAsignacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMatricula = db.Column(db.Integer, db.ForeignKey('matricula.idMatricula', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    idCursoAsignacion = db.Column(db.Integer, db.ForeignKey('asignacion_curso.idCursoAsignacion', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    matricula = db.relationship('Matricula', back_populates='matricula_asignacion')
    asignaciones_curso = db.relationship('AsignacionCurso', back_populates='matricula_asignacion')
    calificacion = db.relationship('Calificacion', backref='matricula_asignacion', uselist=False)

    
class Calificacion(db.Model):
    __tablename__ = 'calificacion'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}

    idCalificacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMatricula = db.Column(
        db.Integer, 
        db.ForeignKey('matricula.idMatricula', ondelete='CASCADE', onupdate='CASCADE'), 
        nullable=False,
    )
    idMatriculaAsignacion = db.Column(
        db.Integer,
        db.ForeignKey('matricula_asignacion.idMatriculaAsignacion', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    NotaAutonoma1 = db.Column(db.Numeric(5, 2), default=0)
    NotaPractica1 = db.Column(db.Numeric(5, 2), default=0)
    NotaLeccion1 = db.Column(db.Numeric(5, 2), default=0)
    NotaExamen1 = db.Column(db.Numeric(5, 2), default=0)
    PromQuimestre1 = db.Column(db.Numeric(5, 2), default=0)
    NotaAutonoma2 = db.Column(db.Numeric(5, 2), default=0)
    NotaPractica2 = db.Column(db.Numeric(5, 2), default=0)
    NotaLeccion2 = db.Column(db.Numeric(5, 2), default=0)
    NotaExamen2 = db.Column(db.Numeric(5, 2), default=0)
    PromQuimestre2 = db.Column(db.Numeric(5, 2), default=0)
    PromedioFinal = db.Column(db.Numeric(5, 2), default=0)


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_collate': 'utf8mb4_spanish_ci'}

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
