import sqlite3


DATABASE = "inventario.db"


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

            carrito_ventas.producto_id,

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
# AGREGAR PRODUCTO AL CARRITO
# ==========================================

def agregar_carrito(producto_id, cantidad, precio, usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    # comprobar stock disponible

    cursor.execute("""
        SELECT nombre, stock
        FROM productos
        WHERE id = ?
    """,
    (producto_id,))


    producto = cursor.fetchone()


    if not producto:
        conexion.close()
        return False


    stock = producto["stock"]



    # cantidad actual en carrito

    cursor.execute("""
        SELECT cantidad
        FROM carrito_ventas
        WHERE producto_id = ?
        AND usuario = ?
    """,
    (
        producto_id,
        usuario
    ))


    existe = cursor.fetchone()



    cantidad_actual = 0


    if existe:

        cantidad_actual = existe["cantidad"]



    nueva_cantidad = cantidad_actual + int(cantidad)



    if nueva_cantidad > stock:

        conexion.close()

        return False



    if existe:


        subtotal = nueva_cantidad * float(precio)


        cursor.execute("""
            UPDATE carrito_ventas

            SET cantidad = ?,
                subtotal = ?

            WHERE producto_id = ?
            AND usuario = ?

        """,
        (
            nueva_cantidad,
            subtotal,
            producto_id,
            usuario
        ))



    else:


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


    return True


# ==========================================
# AUMENTAR CANTIDAD CARRITO
# ==========================================

def aumentar_cantidad(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT cantidad, precio
        FROM carrito_ventas
        WHERE id = ?
    """,
    (id,))


    item = cursor.fetchone()


    if item:

        nueva_cantidad = item["cantidad"] + 1

        nuevo_subtotal = nueva_cantidad * item["precio"]


        cursor.execute("""
            UPDATE carrito_ventas

            SET cantidad = ?,
                subtotal = ?

            WHERE id = ?

        """,
        (
            nueva_cantidad,
            nuevo_subtotal,
            id
        ))



    conexion.commit()

    conexion.close()



# ==========================================
# DISMINUIR CANTIDAD CARRITO
# ==========================================

def disminuir_cantidad(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT cantidad, precio
        FROM carrito_ventas
        WHERE id = ?
    """,
    (id,))


    item = cursor.fetchone()



    if item:


        nueva_cantidad = item["cantidad"] - 1



        if nueva_cantidad <= 0:


            cursor.execute("""
                DELETE FROM carrito_ventas
                WHERE id = ?

            """,
            (id,))


        else:


            nuevo_subtotal = nueva_cantidad * item["precio"]


            cursor.execute("""
                UPDATE carrito_ventas

                SET cantidad = ?,
                    subtotal = ?

                WHERE id = ?

            """,
            (
                nueva_cantidad,
                nuevo_subtotal,
                id
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
# OBTENER TOTAL CARRITO
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