INSERT INTO `administrador` (`idAdministrador`, `Cedula`, `Nombre`, `Apellido`, `Correo`) VALUES
(1, '1100000000', 'Admin', '', 'admin@mail.com');

INSERT INTO `materia` (`idMateria`, `Nombre`, `Descripcion`) VALUES
(3, 'Historia', 'Materia de Historia para 3ro'),
(6, 'Matematica', 'Materia de Matematica para 3ro'),
(7, 'Lengua y Literatura', 'Materia de Lengua y Literatura para 1ro'),
(9, 'Emprendimiento Y Gestión', NULL),
(10, 'Filosofia', 'Materia de Filosofia para 1ro'),
(14, 'Artistica', 'Materia de Artistica para 3ro'),
(16, 'Educacion Fisica', 'Materia de Educacion Fisica para 2do');

INSERT INTO `periodo_lectivo` (`idPeriodo`, `Nombre`, `FechaInicio`, `FechaFin`, `Estado`) VALUES
(1, 'P1 2022', '2022-02-01', '2022-05-31', 'Inactivo'),
(3, 'P2 2022', '2022-10-01', '2023-01-31', 'Inactivo'),
(4, 'P1 2023', '2023-02-01', '2023-05-31', 'Inactivo'),
(6, 'P2 2023', '2023-10-01', '2024-01-31', 'Inactivo'),
(7, 'P1 2024', '2024-02-01', '2024-05-31', 'Inactivo'),
(9, 'P2 2024', '2024-10-01', '2025-01-31', 'Inactivo'),
(10, 'P1 2025', '2025-02-01', '2025-05-31', 'Activo');

INSERT INTO `profesor` (`idProfesor`, `Cedula`, `Nombre`, `Apellido`, `Telefono`, `Correo`, `Especialidad`, `Direccion`) VALUES
(1, '1100000001', 'Juan', 'Pérez', '0990000001', 'juan.perez1@mail.com', 'Educación General', 'Dirección 1'),
(2, '1100000002', 'María', 'Gómez', '0990000002', 'maria.gomez2@mail.com', 'Educación General', 'Dirección 2'),
(3, '1100000003', 'Pedro', 'Rodríguez', '0990000003', 'pedro.rodriguez3@mail.com', 'Educación General', 'Dirección 3'),
(4, '1100000004', 'Luisa', 'López', '0990000004', 'luisa.lopez4@mail.com', 'Educación General', 'Dirección 4'),
(5, '1100000005', 'Carlos', 'Martínez', '0990000005', 'carlos.martinez5@mail.com', 'Educación General', 'Dirección 5'),
(6, '1100000006', 'Ana', 'García', '0990000006', 'ana.garcia6@mail.com', 'Educación General', 'Dirección 6'),
(7, '1100000007', 'Jorge', 'Sánchez', '0990000007', 'jorge.sanchez7@mail.com', 'Educación General', 'Dirección 7'),
(8, '1100000008', 'Marta', 'Ramírez', '0990000008', 'marta.ramirez8@mail.com', 'Educación General', 'Dirección 8'),
(9, '1100000009', 'Luis', 'Torres', '0990000009', 'luis.torres9@mail.com', 'Educación General', 'Dirección 9'),
(10, '1100000010', 'Carmen', 'Vargas', '0990000010', 'carmen.vargas10@mail.com', 'Educación General', 'Dirección 10'),
(11, '1100000011', 'Juan', 'Pérez', '0990000011', 'juan.perez11@mail.com', 'Educación General', 'Dirección 11'),
(12, '1100000012', 'María', 'Gómez', '0990000012', 'maria.gomez12@mail.com', 'Educación General', 'Dirección 12'),
(13, '1100000013', 'Pedro', 'Rodríguez', '0990000013', 'pedro.rodriguez13@mail.com', 'Educación General', 'Dirección 13'),
(14, '1100000014', 'Luisa', 'López', '0990000014', 'luisa.lopez14@mail.com', 'Educación General', 'Dirección 14'),
(15, '1100000015', 'Carlos', 'Martínez', '0990000015', 'carlos.martinez15@mail.com', 'Educación General', 'Dirección 15'),
(16, '1100000016', 'Ana', 'García', '0990000016', 'ana.garcia16@mail.com', 'Educación General', 'Dirección 16'),
(17, '1100000017', 'Jorge', 'Sánchez', '0990000017', 'jorge.sanchez17@mail.com', 'Educación General', 'Dirección 17'),
(18, '1100000018', 'Marta', 'Ramírez', '0990000018', 'marta.ramirez18@mail.com', 'Educación General', 'Dirección 18'),
(19, '1100000019', 'Luis', 'Torres', '0990000019', 'luis.torres19@mail.com', 'Educación General', 'Dirección 19'),
(20, '1100000020', 'Carmen', 'Vargas', '0990000020', 'carmen.vargas20@mail.com', 'Educación General', 'Dirección 20');

INSERT INTO `curso` (`idCurso`, `Nivel`, `Paralelo`) VALUES
(4, '1ro', 'C'),
(1, '2do', 'A');

INSERT INTO `asignacion_curso` (`idAsignacion`, `idProfesor`, `idMateria`, `idCurso`, `Aula`, `HoraEntrada`, `HoraSalida`, `idPeriodo`) VALUES
(1, 1, 3, 4, 'L-102', '19:28:00', '21:28:00', 10);


-- Estudiantes de 1ro A
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310001001', 'Carlos Andrés', 'López Mendoza', '2008-03-15', 'carlos.lopez@estudiantes.edu.ec', '0981001001', 'Av. 10 de Agosto y Eloy Alfaro', 'Participa en clubes de ciencias'),
('1310001002', 'María Fernanda', 'Castro Romero', '2008-05-22', 'maria.castro@estudiantes.edu.ec', '0981001002', 'Cdla. Universitaria, Manta', ''),
('1310001003', 'Luis Eduardo', 'Pérez Almeida', '2008-07-09', 'luis.perez@estudiantes.edu.ec', '0981001003', 'Barrio Jocay, Manta', 'Requiere seguimiento en matemáticas'),
('1310001004', 'Ana Isabel', 'Vera Paredes', '2008-02-17', 'ana.vera@estudiantes.edu.ec', '0981001004', 'Cdla. Los Sauces, Portoviejo', ''),
('1310001005', 'José Miguel', 'García Delgado', '2008-09-03', 'jose.garcia@estudiantes.edu.ec', '0981001005', 'Av. Circunvalación, Manta', ''),
('1310001006', 'Andrea Valeria', 'Zambrano Bravo', '2008-06-30', 'andrea.zambrano@estudiantes.edu.ec', '0981001006', 'Colinas del Sol, Manta', 'Buena participación en clase'),
('1310001007', 'David Sebastián', 'Macías Loor', '2008-08-10', 'david.macias@estudiantes.edu.ec', '0981001007', 'Av. Manabí y San Mateo', ''),
('1310001008', 'Valentina Renata', 'Cedeño Mero', '2008-01-05', 'valentina.cedeno@estudiantes.edu.ec', '0981001008', 'Urbanización Ciudad del Sol', ''),
('1310001009', 'Juan Esteban', 'Moreira Mendoza', '2008-11-19', 'juan.moreira@estudiantes.edu.ec', '0981001009', 'Cdla. Los Ángeles, Portoviejo', ''),
('1310001010', 'Emilia Antonella', 'Alcívar Carreño', '2008-04-24', 'emilia.alcivar@estudiantes.edu.ec', '0981001010', 'Cdla. Santa Martha, Manta', ''),
('1310001011', 'Mateo Joaquín', 'Solórzano Pico', '2008-10-08', 'mateo.solorzano@estudiantes.edu.ec', '0981001011', 'Av. Malecón, Manta', ''),
('1310001012', 'Camila Guadalupe', 'Suárez Cedeño', '2008-03-21', 'camila.suarez@estudiantes.edu.ec', '0981001012', 'Cdla. El Paraíso, Portoviejo', 'Presenta aptitudes artísticas'),
('1310001013', 'Gabriel Alejandro', 'Mejía Pinargote', '2008-07-14', 'gabriel.mejia@estudiantes.edu.ec', '0981001013', 'Barrio Santa Clara, Manta', ''),
('1310001014', 'Isabella Nicole', 'Zamora Giler', '2008-06-04', 'isabella.zamora@estudiantes.edu.ec', '0981001014', 'Cdla. Miraflores, Manta', ''),
('1310001015', 'Daniel Santiago', 'Lucas Mendoza', '2008-09-28', 'daniel.lucas@estudiantes.edu.ec', '0981001015', 'La Pradera, Portoviejo', ''),
('1310001016', 'Sofía María', 'Mendoza Plaza', '2008-05-02', 'sofia.mendoza@estudiantes.edu.ec', '0981001016', 'Cdla. San Alejo, Manta', '');

-- Estudiantes de 1ro B
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310001021', 'Ángel Mauricio', 'López Castro', '2008-01-11', 'angel.lopez@estudiantes.edu.ec', '0981001021', 'Cdla. El Palmar, Manta', ''),
('1310001022', 'Paula Estefanía', 'Zambrano Barreto', '2008-04-05', 'paula.zambrano@estudiantes.edu.ec', '0981001022', 'Cdla. Las Orquídeas, Portoviejo', ''),
('1310001023', 'Sebastián Isaac', 'Cedeño Pico', '2008-03-17', 'sebastian.cedeno@estudiantes.edu.ec', '0981001023', 'Cdla. San Pedro, Manta', ''),
('1310001024', 'Valeria Alejandra', 'Pico Mendoza', '2008-06-22', 'valeria.pico@estudiantes.edu.ec', '0981001024', 'Cdla. Bellavista, Portoviejo', ''),
('1310001025', 'Andrés Felipe', 'González Vera', '2008-08-03', 'andres.gonzalez@estudiantes.edu.ec', '0981001025', 'Cdla. Santa Isabel, Manta', ''),
('1310001026', 'Nicole Sofía', 'Alcócer Mendoza', '2008-10-16', 'nicole.alcocer@estudiantes.edu.ec', '0981001026', 'Cdla. San Rafael, Portoviejo', ''),
('1310001027', 'Marco Antonio', 'Intriago Pincay', '2008-05-26', 'marco.intriago@estudiantes.edu.ec', '0981001027', 'Cdla. Manta Beach', ''),
('1310001028', 'Emily Valentina', 'Bravo Loor', '2008-11-13', 'emily.bravo@estudiantes.edu.ec', '0981001028', 'Cdla. Las Palmas, Manta', ''),
('1310001029', 'Jorge Emilio', 'Plúa Giler', '2008-09-04', 'jorge.plua@estudiantes.edu.ec', '0981001029', 'Cdla. El Retiro, Manta', ''),
('1310001030', 'Karina Beatriz', 'Loor Anchundia', '2008-12-20', 'karina.loor@estudiantes.edu.ec', '0981001030', 'Cdla. Santa Marianita', ''),
('1310001031', 'Pedro Alejandro', 'Giler Moreira', '2008-03-01', 'pedro.giler@estudiantes.edu.ec', '0981001031', 'Cdla. El Murciélago, Manta', ''),
('1310001032', 'Laura Daniela', 'Paredes Mendoza', '2008-07-28', 'laura.paredes@estudiantes.edu.ec', '0981001032', 'Cdla. Los Bosques, Portoviejo', ''),
('1310001033', 'Martín Leonardo', 'Lucas Suárez', '2008-10-02', 'martin.lucas@estudiantes.edu.ec', '0981001033', 'Cdla. Jesús de Nazareth, Manta', ''),
('1310001034', 'Daniela Michelle', 'López Valencia', '2008-01-26', 'daniela.lopez@estudiantes.edu.ec', '0981001034', 'Cdla. Las Cumbres, Portoviejo', ''),
('1310001035', 'Francisco Rafael', 'Chávez Murillo', '2008-06-10', 'francisco.chavez@estudiantes.edu.ec', '0981001035', 'Cdla. El Astillero, Manta', ''),
('1310001036', 'Antonella Belén', 'Mendoza Cedeño', '2008-09-11', 'antonella.mendoza@estudiantes.edu.ec', '0981001036', 'Cdla. Nuevo Manta', '');

-- Estudiantes de 2do A
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310002001', 'Lucas Adrián', 'González Mendoza', '2007-04-11', 'lucas.gonzalez@estudiantes.edu.ec', '0982002001', 'Cdla. Los Esteros, Manta', ''),
('1310002002', 'Daniela Sofía', 'Pico Zambrano', '2007-06-30', 'daniela.pico@estudiantes.edu.ec', '0982002002', 'Cdla. La Victoria, Portoviejo', ''),
('1310002003', 'Matías Alejandro', 'Suárez Vera', '2007-05-14', 'matias.suarez@estudiantes.edu.ec', '0982002003', 'Cdla. Mirador del Río, Manta', ''),
('1310002004', 'Emma Isidora', 'García Macías', '2007-02-28', 'emma.garcia@estudiantes.edu.ec', '0982002004', 'Cdla. La Aurora, Manta', ''),
('1310002005', 'Thiago Esteban', 'Lucas Cedeño', '2007-10-01', 'thiago.lucas@estudiantes.edu.ec', '0982002005', 'Cdla. Urbirríos, Portoviejo', ''),
('1310002006', 'Zoe Daniela', 'López Anchundia', '2007-03-12', 'zoe.lopez@estudiantes.edu.ec', '0982002006', 'Cdla. Nuevo Tarqui, Manta', ''),
('1310002007', 'Cristóbal Elías', 'Chávez Paredes', '2007-08-17', 'cristobal.chavez@estudiantes.edu.ec', '0982002007', 'Cdla. 20 de Mayo, Portoviejo', ''),
('1310002008', 'Isabella Renata', 'Alcívar Zambrano', '2007-09-09', 'isabella.alcivar@estudiantes.edu.ec', '0982002008', 'Cdla. Vista al Mar, Manta', ''),
('1310002009', 'Álvaro Ignacio', 'Zambrano Carreño', '2007-07-05', 'alvaro.zambrano@estudiantes.edu.ec', '0982002009', 'Cdla. Las Palmas, Portoviejo', ''),
('1310002010', 'Martina Lucía', 'Pincay Mera', '2007-11-19', 'martina.pincay@estudiantes.edu.ec', '0982002010', 'Cdla. Ciudadela del Mar, Manta', ''),
('1310002011', 'Samuel Rodrigo', 'Moreira Mendoza', '2007-04-27', 'samuel.moreira@estudiantes.edu.ec', '0982002011', 'Cdla. Los Ceibos, Manta', ''),
('1310002012', 'Julia Rafaela', 'Cedeño Giler', '2007-01-18', 'julia.cedeno@estudiantes.edu.ec', '0982002012', 'Cdla. El Parque, Portoviejo', ''),
('1310002013', 'Iván Gabriel', 'Pico Delgado', '2007-05-03', 'ivan.pico@estudiantes.edu.ec', '0982002013', 'Cdla. Las Delicias, Manta', ''),
('1310002014', 'Victoria Celeste', 'Giler Alcívar', '2007-06-08', 'victoria.giler@estudiantes.edu.ec', '0982002014', 'Cdla. El Florón 5, Portoviejo', ''),
('1310002015', 'Joaquín Eduardo', 'Bravo Solórzano', '2007-03-30', 'joaquin.bravo@estudiantes.edu.ec', '0982002015', 'Cdla. Las Cumbres, Manta', ''),
('1310002016', 'Regina Mariana', 'Delgado Pinargote', '2007-09-22', 'regina.delgado@estudiantes.edu.ec', '0982002016', 'Cdla. Costa Azul, Manta', '');

-- Estudiantes de 2do B
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310002021', 'Leonardo Rafael', 'Zambrano Gómez', '2007-01-03', 'leonardo.zambrano@estudiantes.edu.ec', '0982002021', 'Cdla. Las Palmas, Manta', ''),
('1310002022', 'Julieta Noemí', 'Mera Mendoza', '2007-03-15', 'julieta.mera@estudiantes.edu.ec', '0982002022', 'Cdla. Santa Clara, Portoviejo', ''),
('1310002023', 'Benjamín Ángel', 'Pinargote Vera', '2007-05-27', 'benjamin.pinargote@estudiantes.edu.ec', '0982002023', 'Cdla. San Mateo, Manta', ''),
('1310002024', 'Renata Lucía', 'González Loor', '2007-07-09', 'renata.gonzalez@estudiantes.edu.ec', '0982002024', 'Cdla. Universitaria, Portoviejo', ''),
('1310002025', 'Adrián Fernando', 'Macías Solórzano', '2007-10-12', 'adrian.macias@estudiantes.edu.ec', '0982002025', 'Cdla. El Porvenir, Manta', ''),
('1310002026', 'Natalia Fernanda', 'Barreto Mendoza', '2007-04-06', 'natalia.barreto@estudiantes.edu.ec', '0982002026', 'Cdla. Altamira, Portoviejo', ''),
('1310002027', 'Elías Mauricio', 'Cedeño Bravo', '2007-09-18', 'elias.cedeno@estudiantes.edu.ec', '0982002027', 'Cdla. Los Ángeles, Manta', ''),
('1310002028', 'Victoria Antonia', 'Zamora Parrales', '2007-02-28', 'victoria.zamora@estudiantes.edu.ec', '0982002028', 'Cdla. Portoviejo Norte', ''),
('1310002029', 'Axel Nicolás', 'Paredes Anchundia', '2007-06-20', 'axel.paredes@estudiantes.edu.ec', '0982002029', 'Cdla. Las Orquídeas, Manta', ''),
('1310002030', 'Isidora María', 'Giler Moreira', '2007-08-14', 'isidora.giler@estudiantes.edu.ec', '0982002030', 'Cdla. Las Brisas, Manta', ''),
('1310002031', 'Enzo Alexander', 'Alcívar Zambrano', '2007-12-08', 'enzo.alcivar@estudiantes.edu.ec', '0982002031', 'Cdla. Los Almendros, Manta', ''),
('1310002032', 'Camila Esther', 'Suárez Intriago', '2007-11-01', 'camila.suarez@estudiantes.edu.ec', '0982002032', 'Cdla. Los Olivos, Portoviejo', ''),
('1310002033', 'José Ricardo', 'Cevallos Loor', '2007-03-09', 'jose.cevallos@estudiantes.edu.ec', '0982002033', 'Cdla. El Mirador, Manta', ''),
('1310002034', 'Antonella Judith', 'Delgado Vera', '2007-05-01', 'antonella.delgado@estudiantes.edu.ec', '0982002034', 'Cdla. Nuevo Manta, Manta', ''),
('1310002035', 'Juan Pablo', 'Valencia Carreño', '2007-07-30', 'juan.valencia@estudiantes.edu.ec', '0982002035', 'Cdla. San José, Portoviejo', ''),
('1310002036', 'Bianca Rebeca', 'Plaza Giler', '2007-01-21', 'bianca.plaza@estudiantes.edu.ec', '0982002036', 'Cdla. El Palmar, Manta', '');

-- Estudiantes de 3ro A
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310003001', 'Lucía Fernanda', 'Zambrano Cevallos', '2006-05-10', 'lucia.zambrano@estudiantes.edu.ec', '0983003001', 'Cdla. El Florón, Portoviejo', ''),
('1310003002', 'Diego Andrés', 'Mendoza Vera', '2006-08-22', 'diego.mendoza@estudiantes.edu.ec', '0983003002', 'Cdla. Manta 2000, Manta', ''),
('1310003003', 'Valeria Carolina', 'Pinargote Suárez', '2006-03-18', 'valeria.pinargote@estudiantes.edu.ec', '0983003003', 'Cdla. Los Esteros, Manta', ''),
('1310003004', 'Esteban Gabriel', 'Cedeño López', '2006-10-03', 'esteban.cedeno@estudiantes.edu.ec', '0983003004', 'Cdla. El Paraíso, Portoviejo', ''),
('1310003005', 'Carla Juliana', 'Bravo Anchundia', '2006-07-27', 'carla.bravo@estudiantes.edu.ec', '0983003005', 'Cdla. Las Gaviotas, Manta', ''),
('1310003006', 'Tomás Alejandro', 'Moreira Mera', '2006-01-14', 'tomas.moreira@estudiantes.edu.ec', '0983003006', 'Cdla. Los Almendros, Manta', ''),
('1310003007', 'Camila Alejandra', 'Delgado Intriago', '2006-11-09', 'camila.delgado@estudiantes.edu.ec', '0983003007', 'Cdla. Nueva Esperanza, Portoviejo', ''),
('1310003008', 'José Antonio', 'Zamora Vera', '2006-09-25', 'jose.zamora@estudiantes.edu.ec', '0983003008', 'Cdla. Las Orquídeas, Manta', ''),
('1310003009', 'Martina Isidora', 'Cevallos Barreto', '2006-04-05', 'martina.cevallos@estudiantes.edu.ec', '0983003009', 'Cdla. Santa Clara, Portoviejo', ''),
('1310003010', 'Samuel Ignacio', 'Alcívar Parrales', '2006-06-16', 'samuel.alcivar@estudiantes.edu.ec', '0983003010', 'Cdla. Ciudadela del Sol, Manta', ''),
('1310003011', 'Elena Victoria', 'Mera González', '2006-12-01', 'elena.mera@estudiantes.edu.ec', '0983003011', 'Cdla. El Palmar, Manta', ''),
('1310003012', 'Axel Emmanuel', 'Zambrano Macías', '2006-02-24', 'axel.zambrano@estudiantes.edu.ec', '0983003012', 'Cdla. Universitaria, Portoviejo', ''),
('1310003013', 'Sofía Natalia', 'Pico Loor', '2006-08-04', 'sofia.pico@estudiantes.edu.ec', '0983003013', 'Cdla. Santa Marianita, Manta', ''),
('1310003014', 'Benjamín Isaac', 'Lucas Moreira', '2006-10-27', 'benjamin.lucas@estudiantes.edu.ec', '0983003014', 'Cdla. Nuevo Manta, Manta', ''),
('1310003015', 'Emilia Renata', 'Vera Suárez', '2006-03-11', 'emilia.vera@estudiantes.edu.ec', '0983003015', 'Cdla. Las Palmas, Portoviejo', ''),
('1310003016', 'David Mateo', 'Anchundia Cedeño', '2006-07-01', 'david.anchundia@estudiantes.edu.ec', '0983003016', 'Cdla. Portoviejo Norte', '');

-- Estudiantes de 3ro B
INSERT INTO `estudiante` (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
VALUES 
('1310003021', 'Allison Michelle', 'Loor Zambrano', '2006-04-17', 'allison.loor@estudiantes.edu.ec', '0983003021', 'Cdla. El Parque, Portoviejo', ''),
('1310003022', 'Ángel Sebastián', 'Pico Anchundia', '2006-01-29', 'angel.pico@estudiantes.edu.ec', '0983003022', 'Cdla. Urbirríos, Manta', ''),
('1310003023', 'Javiera Alejandra', 'Mendoza Paredes', '2006-08-11', 'javiera.mendoza@estudiantes.edu.ec', '0983003023', 'Cdla. La Aurora, Portoviejo', ''),
('1310003024', 'Santiago Tomás', 'González Suárez', '2006-03-22', 'santiago.gonzalez@estudiantes.edu.ec', '0983003024', 'Cdla. Costa Azul, Manta', ''),
('1310003025', 'Renata Juliana', 'Macías Alcívar', '2006-09-03', 'renata.macias@estudiantes.edu.ec', '0983003025', 'Cdla. El Mirador, Portoviejo', ''),
('1310003026', 'Lautaro Emanuel', 'Barreto Parrales', '2006-10-14', 'lautaro.barreto@estudiantes.edu.ec', '0983003026', 'Cdla. Los Ceibos, Manta', ''),
('1310003027', 'Emilia Abigail', 'Suárez Vera', '2006-05-05', 'emilia.suarez@estudiantes.edu.ec', '0983003027', 'Cdla. San Mateo, Manta', ''),
('1310003028', 'Joaquín Esteban', 'Lucas Cevallos', '2006-02-08', 'joaquin.lucas@estudiantes.edu.ec', '0983003028', 'Cdla. Bellavista, Portoviejo', ''),
('1310003029', 'Florencia Daniela', 'Giler Mendoza', '2006-11-26', 'florencia.giler@estudiantes.edu.ec', '0983003029', 'Cdla. Altamira, Manta', ''),
('1310003030', 'Tomás Emiliano', 'Chávez Bravo', '2006-06-02', 'tomas.chavez@estudiantes.edu.ec', '0983003030', 'Cdla. Las Gaviotas, Manta', ''),
('1310003031', 'Paula Ignacia', 'Anchundia Loor', '2006-07-15', 'paula.anchundia@estudiantes.edu.ec', '0983003031', 'Cdla. Las Palmas, Portoviejo', ''),
('1310003032', 'Agustín Nicolás', 'Mera Alcívar', '2006-12-21', 'agustin.mera@estudiantes.edu.ec', '0983003032', 'Cdla. Ciudadela del Mar, Manta', ''),
('1310003033', 'Amanda Celeste', 'Vera Solórzano', '2006-03-31', 'amanda.vera@estudiantes.edu.ec', '0983003033', 'Cdla. El Paraíso, Portoviejo', ''),
('1310003034', 'Lucas Adriano', 'Pincay Barreto', '2006-04-23', 'lucas.pincay@estudiantes.edu.ec', '0983003034', 'Cdla. Santa Clara, Manta', ''),
('1310003035', 'Catalina Fabiola', 'Zambrano Suárez', '2006-07-06', 'catalina.zambrano@estudiantes.edu.ec', '0983003035', 'Cdla. Los Ángeles, Portoviejo', ''),
('1310003036', 'Francisco Javier', 'Macías Parrales', '2006-01-11', 'francisco.macias@estudiantes.edu.ec', '0983003036', 'Cdla. Nuevo Tarqui, Manta', '');

INSERT INTO `usuarios` (idUsuario, Username, Password, Rol, Estado, idAdministrador)
VALUES (1, 'admin', '123456superuser', 'Admin', 'Activo', 1);