-- 1. Tabla Estudiante;
CREATE TABLE IF NOT EXISTS Estudiante (
    idEstudiante INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR(20) UNIQUE NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    FechaNacimiento DATE NOT NULL,
    Correo VARCHAR(100) NOT NULL,
    Telefono VARCHAR(20),
    Direccion TEXT NOT NULL,
    Observacion TEXT
) ENGINE=InnoDB;

-- 2. Tabla Profesor;
CREATE TABLE IF NOT EXISTS Profesor (
    idProfesor INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR(20) UNIQUE NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20),
    Correo VARCHAR(100) NOT NULL,
    Especialidad VARCHAR(100) NOT NULL,
    Direccion TEXT
) ENGINE=InnoDB;

-- 3. Tabla Materia;
CREATE TABLE IF NOT EXISTS Materia (
    idMateria INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Nivel ENUM('1ro', '2do', '3ro') NOT NULL,
    Descripcion TEXT
) ENGINE=InnoDB;

-- 4. Asignación de Materias (Profesor-Materia-Curso);
CREATE TABLE IF NOT EXISTS AsignacionMaterias (
    idAsignacion INT AUTO_INCREMENT PRIMARY KEY,
    idProfesor INT NOT NULL,
    idMateria INT NOT NULL,
    idCurso INT NOT NULL,
    FOREIGN KEY (idProfesor) REFERENCES Profesor(idProfesor)
        ON DELETE CASCADE,
    FOREIGN KEY (idMateria) REFERENCES Materia(idMateria)
        ON DELETE CASCADE,
    FOREIGN KEY (idCurso) REFERENCES Curso(idCurso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Tabla PeriodoLectivo;
CREATE TABLE IF NOT EXISTS PeriodoLectivo (
    idPeriodo INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(20) NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaFin DATE NOT NULL,
    Estado ENUM('Activo', 'Inactivo') DEFAULT 'Inactivo'
) ENGINE=InnoDB;

-- 6. Tabla Curso;
CREATE TABLE IF NOT EXISTS Curso (
    idCurso INT AUTO_INCREMENT PRIMARY KEY,
    Paralelo VARCHAR(5) NOT NULL,
    Turno ENUM('Mañana', 'Tarde') NOT NULL,
    Aula VARCHAR(50),
    idPeriodo INT,
    FOREIGN KEY (idPeriodo) REFERENCES PeriodoLectivo(idPeriodo)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 7. Tabla Matrícula;
CREATE TABLE IF NOT EXISTS Matricula (
    idMatricula INT AUTO_INCREMENT PRIMARY KEY,
    idEstudiante INT NOT NULL,
    idCurso INT NOT NULL,
    idPeriodo INT NOT NULL,
    FechaMatricula DATE NOT NULL,
    PromedioAnual DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (idEstudiante) REFERENCES Estudiante(idEstudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (idCurso) REFERENCES Curso(idCurso)
        ON DELETE CASCADE,
    FOREIGN KEY (idPeriodo) REFERENCES PeriodoLectivo(idPeriodo)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. Tabla Calificaciones Quimestre;
CREATE TABLE IF NOT EXISTS CalificacionesQuimestre (
    idQuimestre INT AUTO_INCREMENT PRIMARY KEY,
    idEstudiante INT NOT NULL,
    idMateria INT NOT NULL,
    idCurso INT NOT NULL,
    Quimestre ENUM('1', '2') NOT NULL,
    NotaAutonoma DECIMAL(5,2) DEFAULT 0,
    NotaPractica DECIMAL(5,2) DEFAULT 0,
    NotaLeccion DECIMAL(5,2) DEFAULT 0,
    NotaExamen DECIMAL(5,2) DEFAULT 0,
    PromedioQuimestre DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (idEstudiante) REFERENCES Estudiante(idEstudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (idMateria) REFERENCES Materia(idMateria)
        ON DELETE CASCADE,
    FOREIGN KEY (idCurso) REFERENCES Curso(idCurso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. Tabla Calificaciones Finales;
CREATE TABLE IF NOT EXISTS CalificacionesFinales (
    idCalificacionFinal INT AUTO_INCREMENT PRIMARY KEY,
    idEstudiante INT NOT NULL,
    idMateria INT NOT NULL,
    idCurso INT NOT NULL,
    PromQuimestre1 DECIMAL(5,2) DEFAULT 0,
    PromQuimestre2 DECIMAL(5,2) DEFAULT 0,
    PromedioFinal DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (idEstudiante) REFERENCES Estudiante(idEstudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (idMateria) REFERENCES Materia(idMateria)
        ON DELETE CASCADE,
    FOREIGN KEY (idCurso) REFERENCES Curso(idCurso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. Tabla Usuarios;
CREATE TABLE IF NOT EXISTS Usuarios (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Rol ENUM('Admin', 'Profesor', 'Estudiante') NOT NULL,
    Estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    idPersona INT,
    FOREIGN KEY (idPersona) REFERENCES Estudiante(idEstudiante)
        ON DELETE SET NULL
) ENGINE=InnoDB;
