import sqlite3


DATABASE = "inventario.db"


# ==========================================
# CONEXIÓN
# ==========================================

def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR CARRITO VENTAS
# ==========================================

def listar_carrito(usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT

            carrito_ventas.id,

            productos.nombre AS producto,

            carrito_ventas.cantidad,

            carrito_ventas.precio,

            carrito_ventas.subtotal


        FROM carrito_ventas


        INNER JOIN productos

        ON productos.id = carrito_ventas.producto_id


        WHERE carrito_ventas.usuario = ?

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
        INSERT INTO carrito_ventas
        (
            producto_id,
            cantidad,
            precio,
            subtotal,
            usuario
        )

        VALUES (?, ?, ?, ?, ?)

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
        DELETE FROM carrito_ventas

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

        FROM carrito_ventas

        WHERE usuario = ?

    """,
    (usuario,))


    resultado = cursor.fetchone()


    conexion.close()



    if resultado["total"] is None:

        return 0


    return resultado["total"]