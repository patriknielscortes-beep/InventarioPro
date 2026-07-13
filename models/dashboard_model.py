import sqlite3

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# ESTADÍSTICAS GENERALES
# ==========================================

def obtener_estadisticas():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categorias")
    total_categorias = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marcas")
    total_marcas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM productos
        WHERE stock <= 5
    """)

    stock_bajo = cursor.fetchone()[0]

    conexion.close()

    return {
        "productos": total_productos,
        "categorias": total_categorias,
        "marcas": total_marcas,
        "stock_bajo": stock_bajo
    }


# ==========================================
# PRODUCTOS POR CATEGORÍA
# ==========================================

def productos_por_categoria():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            categorias.nombre,
            COUNT(productos.id)

        FROM categorias

        LEFT JOIN productos
        ON categorias.id = productos.categoria_id

        GROUP BY categorias.id
        ORDER BY categorias.nombre
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# VALOR DEL INVENTARIO
# ==========================================

def valor_inventario():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(stock * precio),0)
        FROM productos
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total


# ==========================================
# MOVIMIENTOS
# ==========================================

def movimientos_tipo():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tipo,
            SUM(cantidad)

        FROM movimientos

        GROUP BY tipo
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# STOCK BAJO
# ==========================================

def productos_stock_bajo():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            nombre,
            stock

        FROM productos

        WHERE stock <= 5

        ORDER BY stock ASC
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# VENTAS DEL DÍA
# ==========================================

def ventas_hoy():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total),0)
        FROM ventas
        WHERE DATE(fecha)=DATE('now')
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total


# ==========================================
# VENTAS DEL MES
# ==========================================

def ventas_mes():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total),0)
        FROM ventas
        WHERE strftime('%Y-%m',fecha)=strftime('%Y-%m','now')
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total


# ==========================================
# PRODUCTOS MÁS VENDIDOS
# ==========================================

def productos_mas_vendidos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            productos.nombre,
            SUM(detalle_ventas.cantidad) AS cantidad

        FROM detalle_ventas

        INNER JOIN productos
            ON productos.id = detalle_ventas.producto_id

        GROUP BY productos.id

        ORDER BY cantidad DESC

        LIMIT 5
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# ÚLTIMAS VENTAS
# ==========================================

def ultimas_ventas():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            folio,
            cliente,
            total,
            fecha

        FROM ventas

        ORDER BY id DESC

        LIMIT 5
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos