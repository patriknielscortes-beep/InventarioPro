import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion


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
# BUSCAR USUARIO
# ==========================================

def buscar_usuario(id):

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
# CREAR USUARIO
# ==========================================

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
            rol,
            foto,
            estado
        )
        VALUES
        (?, ?, ?, ?, 'default.png', 'Activo')
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
# EDITAR USUARIO
# ==========================================

def editar_usuario(id, nombre, usuario, rol):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios

        SET nombre = ?,
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
# CAMBIAR PASSWORD
# ==========================================

def cambiar_password(id, password):

    conexion = conectar()

    cursor = conexion.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute("""
        UPDATE usuarios
        SET password = ?
        WHERE id = ?
    """,
    (
        password_hash,
        id
    ))

    conexion.commit()

    conexion.close()



def cambiar_estado(id, estado):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET estado = ?
        WHERE id = ?
    """,
    (
        estado,
        id
    ))

    conexion.commit()

    conexion.close()

# ==========================================
# CAMBIAR ESTADO
# ==========================================

def cambiar_estado(id, estado):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios

        SET estado = ?

        WHERE id = ?
    """,
    (
        estado,
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
# CAMBIAR PASSWORD
# ==========================================

def cambiar_password(id, password):

    conexion = conectar()

    cursor = conexion.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute("""
        UPDATE usuarios
        SET password = ?
        WHERE id = ?
    """,
    (
        password_hash,
        id
    ))

    conexion.commit()

    conexion.close()



# ==========================================
# CAMBIAR ESTADO
# ==========================================

def cambiar_estado(id, estado):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET estado = ?
        WHERE id = ?
    """,
    (
        estado,
        id
    ))

    conexion.commit()

    conexion.close()

    # ==========================================
# BUSCAR USUARIO POR ID
# ==========================================

def buscar_usuario_id(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id = ?
    """,
    (id,))


    usuario = cursor.fetchone()


    conexion.close()


    return usuario