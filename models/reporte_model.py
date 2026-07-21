import sqlite3


DATABASE = "inventario.db"



# ==========================================
# CONEXIÓN BASE DE DATOS
# ==========================================

def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion





# ==========================================
# REPORTE INVENTARIO
# ==========================================

def inventario_pdf():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            productos.sku,
            productos.nombre,
            categorias.nombre AS categoria,
            marcas.nombre AS marca,
            productos.stock,
            productos.precio

        FROM productos

        INNER JOIN categorias
            ON categorias.id = productos.categoria_id

        INNER JOIN marcas
            ON marcas.id = productos.marca_id

        ORDER BY productos.nombre
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos





# ==========================================
# REPORTE VENTAS
# ==========================================

def reporte_ventas():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            id,
            cliente,
            fecha,
            total,
            usuario,
            forma_pago

        FROM ventas

        ORDER BY fecha DESC
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos





# ==========================================
# REPORTE COMPRAS
# ==========================================

def reporte_compras():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            compras.id,
            proveedores.nombre AS proveedor,
            compras.fecha,
            compras.total,
            compras.usuario

        FROM compras

        INNER JOIN proveedores
            ON proveedores.id = compras.proveedor_id

        ORDER BY compras.fecha DESC
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos