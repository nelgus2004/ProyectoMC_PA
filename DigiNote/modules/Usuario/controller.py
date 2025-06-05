from flask import flash, session
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import Usuario, Estudiante, Administrador, Profesor
from passlib.hash import scrypt
import re

def crear_superadmin():
    if not Usuario.query.filter_by(Username='superAdmin').first():
        admin = Usuario(
            Username='superAdmin',
            Correo='admin@diginote.com',
            Password=scrypt.hash('admin123'),
            Rol='Admin',
            Estado='Activo'
        )
        db.session.add(admin)
        db.session.commit()
        print(" * SuperAdmin creado")
    else:
        print(" * SuperAdmin ya existe")

class AuthController:
    def autenticar_login_usuario(self, request):
        if request.method == 'POST':
            profile = request.form['Profile']
            contrasenia = request.form['Password']

            #Verificar si profile tiene formato de correo electrónico
            is_email = re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", profile)

            usuario = None
            if is_email:
                usuario = Usuario.query.filter_by(Correo=profile).first()
            else:
                usuario = Usuario.query.filter_by(Username=profile).first()
            
            if not usuario:
                return{'mensaje': ('Usuario o contraseña incorrectos','danger'),
                       'exito': False}
            
            if scrypt.verify(contrasenia, usuario.Password):
                session['usuario_id'] = usuario.idUsuario
                session['Username'] = usuario.Username
                session['Correo'] = usuario.Correo
                return{'mensaje': (f'Bienvenido, {usuario.Username}!', 'successful'),
                       'exito': True}
            else:
                return{'mensaje': ('Usuario o contraseña incorrectos','danger'),
                       'exito': False}

    def show_usuario(self):
        usuario_actual = Usuario.query.filter_by(idUsuario=session.get('usuario_id')).first()

        if not usuario_actual:
            return []

        if usuario_actual.Rol == 'Admin':
            usuarios = Usuario.query.all()
            resultado = []

            for u in usuarios:
                nombre_vinculado = "Sin vincular"

                if u.Rol == 'Estudiante' and u.idEstudiante:
                    estudiante = Estudiante.query.get(u.idEstudiante)
                    if estudiante:
                        nombre_vinculado = f"{estudiante.Nombre} {estudiante.Apellido}"

                elif u.Rol == 'Profesor' and u.idProfesor:
                    profesor = Profesor.query.get(u.idProfesor)
                    if profesor:
                        nombre_vinculado = f"{profesor.Nombre} {profesor.Apellido}"

                elif u.Rol == 'Admin' and u.idAdministrador:
                    admin = Administrador.query.get(u.idAdministrador)
                    if admin:
                        nombre_vinculado = f"{admin.Nombre} {admin.Apellido}"

                resultado.append({
                    "idUsuario": u.idUsuario,
                    "Username": u.Username,
                    "Correo": u.Correo,
                    "Rol": u.Rol,
                    "Estado": u.Estado,
                    "UsuarioVinculado": nombre_vinculado
                })
            return resultado

        else:
            return {
                "idUsuario": usuario_actual.idUsuario,
                "Username": usuario_actual.Username,
                "Correo": usuario_actual.Correo,
                "Rol": usuario_actual.Rol,
                "Estado": usuario_actual.Estado
            }

  
    def add_usuario(self, request):
        username = request.form.get('Username')
        correo = request.form.get('Correo')
        password = request.form.get('Password')
        rol = request.form.get('Rol') or 'Invitado'
        estado = request.form.get('Estado') or 'Activo'
        id_estudiante = request.form.get('idEstudiante')
        id_profesor = request.form.get('idProfesor')
        id_admin = request.form.get('idAdministrador')

        if Usuario.query.filter((Usuario.Username == username)).first():
            return {'mensaje': ('El nombre de usuario ya está en uso','info')}

        nuevo_usuario = Usuario(
            Username=username,
            Correo=correo,
            Password=scrypt.hash(password),
            Rol=rol,
            Estado=estado,
            idEstudiante=id_estudiante if rol == 'Estudiante' else None,
            idProfesor=id_profesor if rol == 'Profesor' else None,
            idAdministrador=id_admin if rol == 'Admin' else None
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {'mensaje': ('Usuario registrado correctamente','info')}
    
    def get_usuario_by_id(self, id):
        usuario = Usuario.query.get(id)
        if not usuario:
            return {}

        # Determinar el tipo de vínculo y su valor
        if usuario.idEstudiante:
            name_id = 'idEstudiante'
            id_vinculo = usuario.idEstudiante
        elif usuario.idProfesor:
            name_id = 'idProfesor'
            id_vinculo = usuario.idProfesor
        elif usuario.idAdministrador:
            name_id = 'idAdministrador'
            id_vinculo = usuario.idAdministrador
        else:
            name_id = 'idInvitado'
            id_vinculo = None

        return {
            'idUsuario': usuario.idUsuario,
            'Username': usuario.Username,
            'Correo': usuario.Correo,
            'Rol': usuario.Rol,
            'Estado': usuario.Estado,
            'name_id': name_id,
            'id_vinculo': id_vinculo
        }


    def update_usuario_propio(self, request):
        
        usuario = Usuario.query.filter_by(Username=session.get('Username')).first()
        if not usuario:
            return {'mensaje': ('Usuario no encontrado', 'danger')}

        nuevo_username = request.form.get('Username')
        nueva_password = request.form.get('Password')
        nuevo_correo = request.form.get('Correo')

        if nuevo_username and Usuario.query.filter(Usuario.Username == nuevo_username, Usuario.idUsuario != usuario.idUsuario).first():
            return {'mensaje': ('El nombre de usuario ya está en uso', 'info')}
        
        usuario.Username = nuevo_username or usuario.Username
        usuario.Password = scrypt.hash(nueva_password) if nueva_password else usuario.Password
        usuario.Correo = nuevo_correo or usuario.Correo

        db.session.commit()
        session['Username'] = usuario.Username
        session['Correo'] = usuario.Correo
        
        return {'mensaje': ('Perfil actualizado correctamente', 'successful')}

    def update_usuario_admin(self, id_usuario, request):
        usuario_admin = Usuario.query.filter_by(Username=session.get('Username')).first()
        admin = Usuario.query.get(usuario_admin)

        if not admin or admin.Rol != 'Admin':
            return {'mensaje': ('Acceso denegado', 'danger')}

        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {'mensaje': ('Usuario no encontrado', 'danger')}

        nuevo_username = request.form.get('username')
        nueva_password = request.form.get('password')
        nuevo_correo = request.form.get('correo')

        if nuevo_username and Usuario.query.filter(Usuario.Username == nuevo_username, Usuario.idUsuario != id_usuario).first():
            return {'mensaje': ('El nombre de usuario ya está en uso', 'info')}
        
        usuario.Username = nuevo_username or usuario.Username
        usuario.Password = scrypt.hash(nueva_password) if nueva_password else usuario.Password
        usuario.Correo = nuevo_correo or usuario.Correo

        db.session.commit()
        return {'mensaje': ('Usuario actualizado por admin', 'successful')}


    def delete_usuario(self, id_usuario):
        
        try:
            usuarioAdmin = Usuario.query.filter_by(Username=session.get('Username')).first()

            if not usuarioAdmin or usuarioAdmin.Rol != 'Admin':
                return {'mensaje': ('No tienes permiso para realizar esta acción', 'danger')}

            usuario_a_eliminar = Usuario.query.get(id_usuario)

            if not usuario_a_eliminar:
                return {'mensaje': ('Usuario no encontrado', 'danger')}

            db.session.delete(usuario_a_eliminar)
            db.session.commit()
            return {'mensaje': ('Usuario eliminado correctamente', 'successful')}
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar usuario: {e}')
            return ('ERROR: No se pudo eliminar al usuario.', 'danger')
        

    def solicitar_perfil_estudiante(self, request):
        usuario_id = session.get('usuario_id')
        usuario = Usuario.query.get(usuario_id)

        if not usuario or usuario.Rol != 'Invitado':
            return {'mensaje': ('No tienes permiso para esta acción', 'danger')}

        estudiante = Estudiante(
            Cedula=request.form['Cedula'],
            Nombre=request.form['Nombre'].strip().title(),
            Apellido=request.form['Apellido'].strip().title(),
            FechaNacimiento=request.form['FechaNacimiento'],
            Telefono=request.form.get('Telefono'),
            Direccion=request.form.get('Direccion', ''),
            Observacion=request.form.get('Observacion')
        )
        db.session.add(estudiante)
        db.session.commit()

        # Actualizar usuario
        usuario.Rol = 'Estudiante'
        usuario.idEstudiante = estudiante.idEstudiante
        db.session.commit()

        return {'mensaje': ('Petición de usuario estudiante enviada', 'info')}

    def obtener_vinculado_por_rol(self, rol):
        if rol == 'Estudiante':
            registros = Estudiante.query.filter(Estudiante.usuario == None).all()
            return { 'vinculado': [{'id': e.idEstudiante, 'nombre': f'{e.Apellido} {e.Nombre}'} for e in registros] }
        elif rol == 'Profesor':
            registros = Profesor.query.filter(Profesor.usuario == None).all()
            return { 'vinculado': [{'id': p.idProfesor, 'nombre': f'{p.Apellido} {p.Nombre}'} for p in registros] }
        elif rol == 'Admin':
            registros = Administrador.query.filter(Administrador.usuario == None).all()
            return { 'vinculado': [{'id': a.idAdministrador, 'nombre': f'{a.Apellido} {a.Nombre}'} for a in registros] }
        else:
            return { 'vinculado': [] }
