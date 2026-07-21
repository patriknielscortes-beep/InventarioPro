import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = "inventario.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def buscar_usuario(usuario):
    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()

    conexion.close()

    return resultado


def validar_usuario(usuario, password):

    usuario_db = buscar_usuario(usuario)

    if usuario_db:

        if check_password_hash(usuario_db["password"], password):
            return usuario_db

    return None

# ==========================================
# LISTAR USUARIOS
# ==========================================

def listar_usuarios():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        ORDER BY id DESC
    """)

    usuarios = cursor.fetchall()

    conexion.close()

    return usuarios


# ==========================================
# CREAR USUARIO
# ==========================================

from werkzeug.security import generate_password_hash

def crear_usuario(nombre, usuario, password, rol):

    conexion = conectar()

    cursor = conexion.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO usuarios
        (
            nombre,
            usuario,
            password,
            rol
        )
        VALUES
        (?, ?, ?, ?)
    """,
    (
        nombre,
        usuario,
        password_hash,
        rol
    ))

    conexion.commit()

    conexion.close()


# ==========================================
# BUSCAR USUARIO
# ==========================================

def buscar_usuario_id(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id = ?
    """, (id,))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario


# ==========================================
# EDITAR USUARIO
# ==========================================

def editar_usuario(id, nombre, usuario, rol):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET
            nombre = ?,
            usuario = ?,
            rol = ?
        WHERE id = ?
    """,
    (
        nombre,
        usuario,
        rol,
        id
    ))

    conexion.commit()

    conexion.close()


# ==========================================
# ELIMINAR USUARIO
# ==========================================

def eliminar_usuario(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (id,))

    conexion.commit()

    conexion.close()

    # ==========================================
# ACTUALIZAR FOTO PERFIL
# ==========================================

def actualizar_foto(usuario, foto):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET foto = ?
        WHERE usuario = ?
    """,
    (
        foto,
        usuario
    ))

    conexion.commit()

    conexion.close()


# ==========================================
# CAMBIAR CONTRASEÑA
# ==========================================

def cambiar_password(usuario, password_actual, password_nueva):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT password
        FROM usuarios
        WHERE usuario = ?
    """,
    (usuario,))


    datos = cursor.fetchone()



    if not datos:

        conexion.close()
        return False



    if not check_password_hash(datos["password"], password_actual):

        conexion.close()
        return False



    nueva = generate_password_hash(password_nueva)



    cursor.execute("""
        UPDATE usuarios
        SET password = ?
        WHERE usuario = ?
    """,
    (
        nueva,
        usuario
    ))


    conexion.commit()

    conexion.close()


    return True