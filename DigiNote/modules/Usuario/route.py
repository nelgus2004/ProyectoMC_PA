from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from .controller import AuthController
from ..inicio.route import menu

usuario_bp = Blueprint('auth', __name__, template_folder='DigiNote/templates')
controller = AuthController()

@usuario_bp.route('/logIn', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('inicio.menu'))
    return render_template('auth/login.html')

@usuario_bp.route('/auth_autenticate', methods=['GET', 'POST'])
def login_autenticar():
    result = controller.autenticar_login_usuario(request)
    flash(*result['mensaje'])
    if result['exito']:
        return redirect(url_for('inicio.menu'))
    else:
        return redirect(url_for('auth.login'))

@usuario_bp.route('/logOut',  methods=['GET'])
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente.', 'successful')
    return redirect(url_for('auth.login'))

@usuario_bp.route('/registrar', methods=['GET', 'POST'])
def register_external():
    if 'usuario_id' in session:
        return redirect(url_for('inicio.menu'))
    return render_template('auth/registrar.html')

@usuario_bp.route('/auth_add', methods=['GET', 'POST'])
def add_usuario():
    result = controller.add_usuario(request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show_usuario'))
            
@usuario_bp.route('/auth_show', methods=['GET', 'POST'])
def show_usuario():
    result = controller.show_usuario()
    return render_template(
        'usuario.html', 
        active_page='user', 
        registros=result,
        r_add=url_for('auth.add_usuario'),
        r_get=url_for('auth.get_usuario', id_usuario=0).rsplit('/', 1)[0],
        r_updatePropio=url_for('auth.update_usuario_propio'),
        r_updateAdmin=url_for('auth.update_usuarios', id_usuario=0).rsplit('/', 1)[0],
        r_delete=url_for('auth.delete_usuario', id_usuario=0).rsplit('/', 1)[0],
        vinculado=url_for('auth.obtener_vinculo_por_rol', rol='ROL')
    )

@usuario_bp.route('/get_usuario/<int:id_usuario>', methods=['GET', 'POST'])
def get_usuario(id):
    result = controller.get_usuario_by_id(id)
    if result:
        return jsonify(result)
    return jsonify({}), 404

@usuario_bp.route('/admin/auth_update/<int:id_usuario>', methods=['POST'])
def update_usuarios(id_usuario):
    result = controller.update_usuario_admin(id_usuario, request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show_usuario'))

@usuario_bp.route('/profile/auth_update', methods=['POST'])
def update_usuario_propio():
    result = controller.update_usuario_propio(request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show_usuario'))

@usuario_bp.route('/auth_delete/<int:id_usuario>', methods=['POST'])
def delete_usuario(id_usuario):
    print('***************************************************')
    result = controller.delete_usuario(id_usuario)
    print(result)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show_usuario'))

@usuario_bp.route('/solicitud/estudiante', methods=['POST'])
def solicitar_estudiante():
    result = controller.solicitar_perfil_estudiante(request)
    flash(*result['mensaje'])
    return redirect(url_for('inicio.menu'))

@usuario_bp.route('/datos_vinculados/<rol>', methods=['POST', 'GET'])
def obtener_vinculo_por_rol(rol):
    result = controller.obtener_vinculado_por_rol(rol)
    return jsonify(result)