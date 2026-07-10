import sqlite3

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row

    return conexion


def obtener_estadisticas():

    conexion = conectar()
    cursor = conexion.cursor()

    # Total productos
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]

    # Total categorías
    cursor.execute("SELECT COUNT(*) FROM categorias")
    total_categorias = cursor.fetchone()[0]

    # Total marcas
    cursor.execute("SELECT COUNT(*) FROM marcas")
    total_marcas = cursor.fetchone()[0]

    # Productos con stock bajo (5 o menos)
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

    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

# ==========================================
# VALOR TOTAL INVENTARIO
# ==========================================

def valor_inventario():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            SUM(stock * precio)
        FROM productos
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total or 0



# ==========================================
# ENTRADAS Y SALIDAS
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
# PRODUCTOS CON STOCK BAJO
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