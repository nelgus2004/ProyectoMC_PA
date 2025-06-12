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


            
@usuario_bp.route('/show_usuario', methods=['GET', 'POST'])
def show():
    result = controller.show_usuario()
    return render_template(
        'usuario.html', 
        active_page='user', 
        registros=result,
        r_add=url_for('auth.add'),
        r_get=url_for('auth.get', id_usuario=0).rsplit('/', 1)[0],
        r_updatePropio=url_for('auth.update_usuario_propio'),
        r_updateAdmin=url_for('auth.update', id_usuario=0).rsplit('/', 1)[0],
        r_delete=url_for('auth.delete', id_usuario=0).rsplit('/', 1)[0]
    )
    
@usuario_bp.route('/add_usuario', methods=['GET', 'POST'])
def add():
    result = controller.add_usuario(request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show'))

@usuario_bp.route('/get_usuario/<int:id_usuario>', methods=['GET', 'POST'])
def get(id_usuario):
    result = controller.get_usuario_by_id(id_usuario)
    if result:
        return jsonify(result)
    return jsonify({}), 404

@usuario_bp.route('/admin/update_usuarios/<int:id_usuario>', methods=['POST'])
def update(id_usuario):
    result = controller.update_usuario_admin(id_usuario, request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show'))

@usuario_bp.route('/profile/update_usuario', methods=['POST'])
def update_usuario_propio():
    result = controller.update_usuario_propio(request)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show'))

@usuario_bp.route('/delete_usuario/<int:id_usuario>', methods=['POST', 'GET'])
def delete(id_usuario):
    result = controller.delete_usuario(id_usuario)
    print(result)
    flash(*result['mensaje'])
    return redirect(url_for('auth.show'))

@usuario_bp.route('/solicitud/estudiante', methods=['POST'])
def solicitar_estudiante():
    result = controller.solicitar_perfil_estudiante(request)
    flash(*result['mensaje'])
    return redirect(url_for('inicio.menu'))

@usuario_bp.route('/datos_vinculados/<rol>', methods=['POST', 'GET'])
def obtener_vinculo_por_rol(rol):
    result = controller.obtener_vinculado_por_rol(rol)
    print(result)
    return jsonify(result)