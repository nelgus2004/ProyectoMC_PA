-- 1. Tabla Estudiante;
CREATE TABLE IF NOT EXISTS Estudiante (
    ID_Estudiante INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR(20) UNIQUE NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    FechaNacimiento DATE,
    Correo VARCHAR(100),
    Telefono VARCHAR(20),
    Direccion TEXT,
    Observacion TEXT
) ENGINE=InnoDB;

-- 2. Tabla Profesor;
CREATE TABLE IF NOT EXISTS Profesor (
    ID_Profesor INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR(20) UNIQUE NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20),
    Correo VARCHAR(100),
    Especialidad VARCHAR(100),
    Direccion TEXT
) ENGINE=InnoDB;

-- 3. Tabla Materia;
CREATE TABLE IF NOT EXISTS Materia (
    ID_Materia INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Nivel ENUM('1ro', '2do', '3ro') NOT NULL,
    Descripcion TEXT
) ENGINE=InnoDB;

-- 4. Tabla PeriodoLectivo;
CREATE TABLE IF NOT EXISTS PeriodoLectivo (
    ID_Periodo INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(20) NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaFin DATE NOT NULL,
    Estado ENUM('Activo', 'Inactivo') DEFAULT 'Inactivo'
) ENGINE=InnoDB;

-- 5. Tabla Curso;
CREATE TABLE IF NOT EXISTS Curso (
    ID_Curso INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Grado VARCHAR(20) NOT NULL,
    Turno ENUM('Mañana', 'Tarde') NOT NULL,
    Aula VARCHAR(50),
    ID_Periodo INT,
    FOREIGN KEY (ID_Periodo) REFERENCES PeriodoLectivo(ID_Periodo)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 6. Tabla Matrícula;
CREATE TABLE IF NOT EXISTS Matricula (
    ID_Matricula INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT NOT NULL,
    ID_Curso INT NOT NULL,
    ID_Periodo INT NOT NULL,
    FechaMatricula DATE NOT NULL,
    PromedioAnual DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (ID_Estudiante) REFERENCES Estudiante(ID_Estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Periodo) REFERENCES PeriodoLectivo(ID_Periodo)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. Asignación de Materias (Profesor-Materia-Curso);
CREATE TABLE IF NOT EXISTS AsignacionMaterias (
    ID_Asignacion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Profesor INT NOT NULL,
    ID_Materia INT NOT NULL,
    ID_Curso INT NOT NULL,
    FOREIGN KEY (ID_Profesor) REFERENCES Profesor(ID_Profesor)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Materia) REFERENCES Materia(ID_Materia)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. Tabla Calificaciones Quimestre;
CREATE TABLE IF NOT EXISTS CalificacionesQuimestre (
    ID_Quimestre INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT NOT NULL,
    ID_Materia INT NOT NULL,
    ID_Curso INT NOT NULL,
    Quimestre ENUM('1', '2') NOT NULL,
    NotaAutonoma DECIMAL(5,2) DEFAULT 0,
    NotaPractica DECIMAL(5,2) DEFAULT 0,
    NotaLeccion DECIMAL(5,2) DEFAULT 0,
    NotaExamen DECIMAL(5,2) DEFAULT 0,
    PromedioQuimestre DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (ID_Estudiante) REFERENCES Estudiante(ID_Estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Materia) REFERENCES Materia(ID_Materia)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. Tabla Calificaciones Finales;
CREATE TABLE IF NOT EXISTS CalificacionesFinales (
    ID_CalificacionFinal INT AUTO_INCREMENT PRIMARY KEY,
    ID_Estudiante INT NOT NULL,
    ID_Materia INT NOT NULL,
    ID_Curso INT NOT NULL,
    PromQuimestre1 DECIMAL(5,2) DEFAULT 0,
    PromQuimestre2 DECIMAL(5,2) DEFAULT 0,
    PromedioFinal DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (ID_Estudiante) REFERENCES Estudiante(ID_Estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Materia) REFERENCES Materia(ID_Materia)
        ON DELETE CASCADE,
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. Tabla Usuarios;
CREATE TABLE IF NOT EXISTS Usuarios (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Rol ENUM('Admin', 'Profesor', 'Estudiante') NOT NULL,
    Estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    ID_Persona INT,
    FOREIGN KEY (ID_Persona) REFERENCES Estudiante(ID_Estudiante)
        ON DELETE SET NULL
) ENGINE=InnoDB;
