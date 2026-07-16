import sqlite3
from datetime import datetime

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# REGISTRAR ENVÍO
# ==========================================

def registrar_envio(
        venta_id,
        correo,
        estado,
        detalle=""):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO envios_correo
        (
            venta_id,
            correo,
            fecha,
            estado,
            detalle
        )

        VALUES (?, ?, ?, ?, ?)
    """,
    (
        venta_id,
        correo,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        estado,
        detalle
    ))

    conexion.commit()
    conexion.close()


# ==========================================
# LISTAR ENVÍOS
# ==========================================

def listar_envios():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM envios_correo
        ORDER BY id DESC
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos