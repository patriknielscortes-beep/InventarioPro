import sqlite3
from datetime import datetime


DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR COMPRAS
# ==========================================

def listar_compras():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            compras.*,
            proveedores.nombre AS proveedor

        FROM compras

        LEFT JOIN proveedores

        ON compras.proveedor_id = proveedores.id

        ORDER BY compras.id DESC

    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos



# ==========================================
# CREAR COMPRA
# ==========================================

def crear_compra(proveedor_id, total, usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    fecha = datetime.now().strftime("%d-%m-%Y %H:%M")


    cursor.execute("""
        INSERT INTO compras
        (
            proveedor_id,
            fecha,
            total,
            usuario
        )

        VALUES
        (?, ?, ?, ?)

    """,
    (
        proveedor_id,
        fecha,
        total,
        usuario
    ))


    compra_id = cursor.lastrowid


    conexion.commit()

    conexion.close()


    return compra_id


# ==========================================
#  DETALLE COMPRA
# ==========================================


def detalle_compra(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT

            detalle_compras.*,

            productos.nombre AS producto


        FROM detalle_compras


        INNER JOIN productos

        ON detalle_compras.producto_id = productos.id


        WHERE detalle_compras.compra_id = ?


    """,
    (id,))


    datos = cursor.fetchall()


    conexion.close()


    return datos

# ==========================================
# AGREGAR DETALLE COMPRA
# ==========================================

def agregar_detalle(
    compra_id,
    producto_id,
    cantidad,
    precio,
    usuario
):

    conexion = conectar()

    cursor = conexion.cursor()


    subtotal = int(cantidad) * float(precio)


    # Guardar detalle compra
    cursor.execute("""
        INSERT INTO detalle_compras
        (
            compra_id,
            producto_id,
            cantidad,
            precio,
            subtotal
        )

        VALUES
        (?, ?, ?, ?, ?)

    """,
    (
        compra_id,
        producto_id,
        cantidad,
        precio,
        subtotal
    ))


    # Actualizar stock

    cursor.execute("""
        UPDATE productos

        SET stock = stock + ?

        WHERE id = ?

    """,
    (
        cantidad,
        producto_id
    ))



    # Crear movimiento automático

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

    """,
    (
        producto_id,
        "Entrada",
        cantidad,
        datetime.now().strftime("%d-%m-%Y %H:%M"),
        usuario
    ))



    conexion.commit()

    conexion.close()