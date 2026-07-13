import sqlite3

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# LISTAR CARRITO
# ==========================================

def listar_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            carrito_ventas.*,
            productos.nombre AS producto
        FROM carrito_ventas

        INNER JOIN productos
        ON carrito_ventas.producto_id = productos.id

        WHERE carrito_ventas.usuario = ?

        ORDER BY carrito_ventas.id DESC
    """, (usuario,))

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# AGREGAR AL CARRITO
# ==========================================

def agregar_carrito(producto_id, cantidad, precio, usuario):

    conexion = conectar()

    cursor = conexion.cursor()

    subtotal = int(cantidad) * float(precio)

    cursor.execute("""
        INSERT INTO carrito_ventas
        (
            producto_id,
            cantidad,
            precio,
            subtotal,
            usuario
        )
        VALUES
        (?, ?, ?, ?, ?)
    """,
    (
        producto_id,
        cantidad,
        precio,
        subtotal,
        usuario
    ))

    conexion.commit()
    conexion.close()


# ==========================================
# ELIMINAR DEL CARRITO
# ==========================================

def eliminar_carrito(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM carrito_ventas
        WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()


# ==========================================
# VACIAR CARRITO
# ==========================================

def vaciar_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM carrito_ventas
        WHERE usuario = ?
    """, (usuario,))

    conexion.commit()
    conexion.close()


# ==========================================
# TOTAL DEL CARRITO
# ==========================================

def obtener_total_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT SUM(subtotal)
        FROM carrito_ventas
        WHERE usuario = ?
    """, (usuario,))

    total = cursor.fetchone()[0]

    conexion.close()

    if total is None:
        return 0

    return total