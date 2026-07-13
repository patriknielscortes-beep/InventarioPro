import sqlite3
from datetime import datetime


DATABASE = "inventario.db"


# ==========================================
# CONEXIÓN
# ==========================================

def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR VENTAS
# ==========================================

def listar_ventas():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM ventas
        ORDER BY id DESC
    """)


    ventas = cursor.fetchall()


    conexion.close()


    return ventas



# ==========================================
# CREAR VENTA
# ==========================================

def crear_venta(cliente, total, usuario, forma_pago):

    conexion = conectar()

    cursor = conexion.cursor()


    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # IVA Chile 19%

    neto = total / 1.19

    iva = total - neto



    cursor.execute("""
        INSERT INTO ventas
        (
            cliente,
            fecha,
            total,
            usuario,
            forma_pago,
            neto,
            iva
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """,
    (
        cliente,
        fecha,
        total,
        usuario,
        forma_pago,
        neto,
        iva
    ))


    venta_id = cursor.lastrowid


    folio = f"{venta_id:06d}"


    cursor.execute("""
        UPDATE ventas
        SET folio = ?

        WHERE id = ?

    """,
    (
        folio,
        venta_id
    ))


    conexion.commit()

    conexion.close()


    return venta_id



# ==========================================
# AGREGAR DETALLE VENTA
# ==========================================

def agregar_detalle_venta(
        venta_id,
        producto_id,
        cantidad,
        precio):


    conexion = conectar()

    cursor = conexion.cursor()


    subtotal = cantidad * precio


    cursor.execute("""
        INSERT INTO detalle_ventas
        (
            venta_id,
            producto_id,
            cantidad,
            precio,
            subtotal
        )

        VALUES (?, ?, ?, ?, ?)

    """,
    (
        venta_id,
        producto_id,
        cantidad,
        precio,
        subtotal
    ))


    conexion.commit()

    conexion.close()



# ==========================================
# DETALLE VENTA AGRUPADO
# ==========================================

def detalle_venta(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            productos.nombre,

            SUM(detalle_ventas.cantidad)
            AS cantidad,

            detalle_ventas.precio,

            SUM(detalle_ventas.subtotal)
            AS subtotal


        FROM detalle_ventas


        INNER JOIN productos

        ON detalle_ventas.producto_id = productos.id


        WHERE detalle_ventas.venta_id = ?


        GROUP BY
            detalle_ventas.producto_id,
            detalle_ventas.precio

    """,
    (id,))


    detalle = cursor.fetchall()


    conexion.close()


    return detalle

# ==========================================
# ANULAR VENTA
# ==========================================

def anular_venta(id):

    conexion = conectar()

    cursor = conexion.cursor()


    # Obtener productos vendidos

    cursor.execute("""
        SELECT
            producto_id,
            cantidad

        FROM detalle_ventas

        WHERE venta_id = ?

    """,
    (id,))


    detalle = cursor.fetchall()



    # Cambiar estado de venta

    cursor.execute("""
        UPDATE ventas

        SET estado = 'Anulada'

        WHERE id = ?

    """,
    (id,))



    # Devolver stock

    for item in detalle:


        cursor.execute("""
            UPDATE productos

            SET stock = stock + ?

            WHERE id = ?

        """,
        (
            item["cantidad"],
            item["producto_id"]
        ))



    conexion.commit()

    conexion.close()

    return detalle

# ==========================================
# OBTENER VENTA
# ==========================================

def obtener_venta(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM ventas
        WHERE id = ?

    """,
    (id,))


    venta = cursor.fetchone()


    conexion.close()


    return venta