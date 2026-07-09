import sqlite3
from datetime import datetime

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# LISTAR MOVIMIENTOS
# ==========================================

def listar_movimientos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            movimientos.*,
            productos.nombre AS producto

        FROM movimientos

        INNER JOIN productos
        ON movimientos.producto_id = productos.id

        ORDER BY movimientos.id DESC
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# REGISTRAR MOVIMIENTO
# ==========================================

def registrar_movimiento(producto_id, tipo, cantidad, usuario):

    conexion = conectar()

    cursor = conexion.cursor()

    # Obtener stock actual
    cursor.execute("""
        SELECT stock
        FROM productos
        WHERE id = ?
    """, (producto_id,))

    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        return False

    stock_actual = producto["stock"]

    if tipo == "Entrada":
        nuevo_stock = stock_actual + int(cantidad)
    else:
        nuevo_stock = stock_actual - int(cantidad)

        if nuevo_stock < 0:
            conexion.close()
            return False

    # Actualizar stock
    cursor.execute("""
        UPDATE productos
        SET stock = ?
        WHERE id = ?
    """, (nuevo_stock, producto_id))

    # Guardar movimiento
    cursor.execute("""
        INSERT INTO movimientos
        (
            producto_id,
            tipo,
            cantidad,
            fecha,
            usuario
        )
        VALUES
        (?, ?, ?, ?, ?)
    """, (
        producto_id,
        tipo,
        cantidad,
        datetime.now().strftime("%d-%m-%Y %H:%M"),
        usuario
    ))

    conexion.commit()
    conexion.close()

    return True