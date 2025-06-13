# DigitalNoteSys


### Base de datos
Para utilizar la base de datos es necesario crearla manualmente desde
una terminal de MySQL:  mysql -u root -p

```bash
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS db_notas CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;

-- Crear usuario y otorgar privilegios
CREATE USER IF NOT EXISTS 'adminNotes'@'localhost' IDENTIFIED BY 'admin123.';
GRANT ALL PRIVILEGES ON db_notas.* TO 'adminNotes'@'localhost';
FLUSH PRIVILEGES;

```

Si requieres revisar que se creo el usuario y sus privilegios ejecuta lo siguiente:

```bash
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'adminNotes'@'localhost';

```

Usuario Administrador por defecto
```bash
Usuario =   superAdmin
Correro =   admin@diginote.com
Contraseña =   admin123
```