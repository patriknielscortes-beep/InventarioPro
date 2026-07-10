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

# ==========================================
# MOVIMIENTOS POR PRODUCTO
# ==========================================
def movimientos_por_producto(producto_id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            movimientos.*,
            productos.nombre AS producto

        FROM movimientos

        INNER JOIN productos
        ON movimientos.producto_id = productos.id

        WHERE movimientos.producto_id = ?

        ORDER BY movimientos.id DESC

    """,
    (producto_id,))


    datos = cursor.fetchall()


    conexion.close()


    return datos if datos else []

# ==========================================
# RESUMEN DE MOVIMIENTOS PRODUCTO
# ==========================================

def resumen_producto(producto_id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN tipo = 'Entrada' THEN cantidad ELSE 0 END),0) AS entradas,
            COALESCE(SUM(CASE WHEN tipo = 'Salida' THEN cantidad ELSE 0 END),0) AS salidas
        FROM movimientos
        WHERE producto_id = ?
    """,
    (producto_id,))


    resumen = cursor.fetchone()


    cursor.execute("""
        SELECT 
            nombre,
            stock
        FROM productos
        WHERE id = ?
    """,
    (producto_id,))


    producto = cursor.fetchone()


    conexion.close()


    return producto, resumen