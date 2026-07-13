import sqlite3


DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR CARRITO COMPRAS
# ==========================================

def listar_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            carrito_compras.*,
            productos.nombre AS producto

        FROM carrito_compras

        INNER JOIN productos
        ON carrito_compras.producto_id = productos.id

        WHERE carrito_compras.usuario = ?

        ORDER BY carrito_compras.id DESC

    """,
    (usuario,))


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
        INSERT INTO carrito_compras
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
        DELETE FROM carrito_compras
        WHERE id = ?

    """,
    (id,))


    conexion.commit()

    conexion.close()



# ==========================================
# VACIAR CARRITO
# ==========================================

def vaciar_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        DELETE FROM carrito_compras
        WHERE usuario = ?

    """,
    (usuario,))


    conexion.commit()

    conexion.close()



# ==========================================
# TOTAL CARRITO
# ==========================================

def obtener_total_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT SUM(subtotal) AS total

        FROM carrito_compras

        WHERE usuario = ?

    """,
    (usuario,))


    resultado = cursor.fetchone()


    conexion.close()


    if resultado["total"] is None:

        return 0


    return resultado["total"]