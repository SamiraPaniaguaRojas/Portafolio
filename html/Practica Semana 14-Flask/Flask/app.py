from flask import Flask, request, jsonify, render_template
from conexion import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambia esta clave por una segura

# Decorador para proteger rutas con token JWT
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs): 
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Espera formato: Bearer <token>
        if not token:
            return jsonify({'mensaje': 'Token es requerido'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM estudiantes WHERE id=%s", (data['id'],))
                usuario = cursor.fetchone()
            conexion.close()
            if not usuario:
                return jsonify({'mensaje': 'Usuario no encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Token inválido'}), 401
        return f(usuario, *args, **kwargs)
    return decorador

@app.route('/')
def index():
    return render_template('login.html')

# Endpoint de prueba para verificar conexión
@app.route('/test_db')
def test_db():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DESCRIBE estudiantes")
            estructura = cursor.fetchall()
        conexion.close()
        return jsonify({'estructura': estructura})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para registrar usuario
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    nombre_usuario = datos.get('nombre_usuario')
    password = datos.get('password')

    if not nombre_usuario or not password:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    password_hash = generate_password_hash(password)
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO estudiantes (usuario, password) VALUES (%s, %s)",
                           (nombre_usuario, password_hash))
        conexion.commit()
    except pymysql.err.IntegrityError as e:
        return jsonify({'mensaje': 'Usuario ya registrado'}), 400
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        return jsonify({'mensaje': f'Error en base de datos: {str(e)}'}), 500
    finally:
        conexion.close()

    return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201

# Ruta para login y obtención de token
@app.route('/login', methods=['POST'])
def login():
    try:
        datos = request.get_json()
        nombre_usuario = datos.get('nombre_usuario')
        password = datos.get('password')

        if not nombre_usuario or not password:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM estudiantes WHERE usuario=%s", (nombre_usuario,))
            usuario = cursor.fetchone()
        conexion.close()

        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 401
            
        if not check_password_hash(usuario['password'], password):
            return jsonify({'mensaje': 'Contraseña incorrecta'}), 401

        token = jwt.encode({
            'id': usuario['id'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})
        
    except Exception as e:
        print(f"Error en login: {str(e)}")
        return jsonify({'mensaje': f'Error en login: {str(e)}'}), 500

# Ruta protegida: formulario de datos personales
@app.route('/datos', methods=['GET'])
def datos_personales():
    return render_template('datos.html')

# Nueva ruta para obtener datos del usuario autenticado
@app.route('/obtener_usuario', methods=['GET'])
@token_requerido
def obtener_usuario(usuario):
    return jsonify({
        'usuario': usuario['usuario'],
        'nombre': usuario['nombre'],
        'direccion': usuario['direccion'],
        'ciudad': usuario['ciudad']
    })

# Ruta para guardar datos personales
@app.route('/guardar_datos', methods=['POST'])
@token_requerido
def guardar_datos(usuario):
    datos = request.get_json()
    nombre = datos.get('nombre')
    direccion = datos.get('direccion')
    ciudad = datos.get('ciudad')

    if not nombre or not direccion or not ciudad:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE estudiantes SET nombre=%s, direccion=%s, ciudad=%s WHERE id=%s",
                (nombre, direccion, ciudad, usuario['id'])
            )
        conexion.commit()
    finally:
        conexion.close()

    return jsonify({'mensaje': 'Datos guardados correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True) 





