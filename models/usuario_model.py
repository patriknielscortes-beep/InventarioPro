import sqlite3
from werkzeug.security import check_password_hash


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