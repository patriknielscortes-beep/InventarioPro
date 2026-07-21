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

        WHERE stock > 0
        AND stock <= 5

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

# ==========================================
# TOTAL CLIENTES
# ==========================================

def total_clientes():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM clientes
    """)


    total = cursor.fetchone()[0]


    conexion.close()


    return total



# ==========================================
# TOTAL VENTAS
# ==========================================

def total_ventas():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM ventas
    """)


    total = cursor.fetchone()[0]


    conexion.close()


    return total



# ==========================================
# PRODUCTOS AGOTADOS
# ==========================================

def productos_agotados():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM productos
        WHERE stock = 0
    """)


    total = cursor.fetchone()[0]


    conexion.close()


    return total



# ==========================================
# VENTAS ÚLTIMOS 7 DÍAS
# ==========================================

def ventas_ultimos_7_dias():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            DATE(fecha),
            SUM(total)

        FROM ventas

        WHERE fecha >= DATE('now','-6 day')

        GROUP BY DATE(fecha)

        ORDER BY DATE(fecha)

    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos

# ==========================================
# COMPRAS DEL MES
# ==========================================

def compras_mes():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT COALESCE(SUM(total),0)

        FROM compras

        WHERE strftime('%Y-%m',fecha)
        =
        strftime('%Y-%m','now')
    """)


    total = cursor.fetchone()[0]


    conexion.close()


    return total


# ==========================================
# VENTAS VS COMPRAS POR MES
# ==========================================

def ventas_compras_mes():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT 
            mes,
            SUM(ventas),
            SUM(compras)

        FROM (

            SELECT 
                strftime('%Y-%m', fecha) AS mes,
                total AS ventas,
                0 AS compras

            FROM ventas

            WHERE fecha IS NOT NULL


            UNION ALL


            SELECT
                strftime('%Y-%m', fecha) AS mes,
                0 AS ventas,
                total AS compras

            FROM compras

            WHERE fecha IS NOT NULL

        )

        WHERE mes IS NOT NULL

        GROUP BY mes

        ORDER BY mes

    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos


# ==========================================
# GANANCIAS POR MES
# ==========================================

def ganancias_por_mes():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            mes,
            SUM(ventas),
            SUM(compras),
            SUM(ventas)-SUM(compras)

        FROM (

            SELECT
                strftime('%Y-%m', fecha) AS mes,
                total AS ventas,
                0 AS compras

            FROM ventas

            WHERE fecha IS NOT NULL
            AND strftime('%Y-%m', fecha) IS NOT NULL



            UNION ALL



            SELECT
                strftime('%Y-%m', fecha) AS mes,
                0 AS ventas,
                total AS compras

            FROM compras

            WHERE fecha IS NOT NULL
            AND strftime('%Y-%m', fecha) IS NOT NULL

        )

        WHERE mes IS NOT NULL

        GROUP BY mes

        ORDER BY mes

    """)


    datos = cursor.fetchall()

    conexion.close()

    return datos

# ==========================================
# TOP 5 VENDEDORES
# ==========================================

def top_vendedores():

    conexion = conectar()
    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            usuario,
            SUM(total) AS vendido

        FROM ventas

        GROUP BY usuario

        ORDER BY vendido DESC

        LIMIT 5
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos


# ==========================================
# ÚLTIMO PRODUCTO
# ==========================================

def ultimo_producto():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""

        SELECT nombre

        FROM productos

        ORDER BY id DESC

        LIMIT 1

    """)

    dato = cursor.fetchone()

    conexion.close()

    return dato[0] if dato else "Sin registros"


# ==========================================
# ÚLTIMO CLIENTE
# ==========================================

def ultimo_cliente():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""

        SELECT nombre

        FROM clientes

        ORDER BY id DESC

        LIMIT 1

    """)

    dato = cursor.fetchone()

    conexion.close()

    return dato[0] if dato else "Sin registros"


# ==========================================
# ÚLTIMA COMPRA
# ==========================================

def ultima_compra():

    conexion = conectar()
    cursor = conexion.cursor()


    cursor.execute("""
        SELECT total

        FROM compras

        ORDER BY id DESC

        LIMIT 1
    """)


    dato = cursor.fetchone()


    conexion.close()


    if dato and dato[0]:
        return dato[0]

    return 0.0

# ==========================================
# ACTIVIDAD RECIENTE
# ==========================================

def actividad_reciente():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            usuario,
            modulo,
            accion,
            fecha

        FROM auditoria

        ORDER BY id DESC

        LIMIT 5
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos

# ==========================================
# DATOS USUARIO ACTUAL
# ==========================================

def obtener_usuario(usuario):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            nombre,
            usuario,
            rol,
            foto,
            estado

        FROM usuarios

        WHERE usuario = ?

    """,(usuario,))


    dato = cursor.fetchone()


    conexion.close()


    return dato

# ==========================================
# NOTIFICACIONES DASHBOARD
# ==========================================

def obtener_notificaciones():

    conexion = conectar()

    cursor = conexion.cursor()


    notificaciones = []



    # STOCK BAJO

    cursor.execute("""
        SELECT nombre, stock
        FROM productos
        WHERE stock > 0
        AND stock <= 5
        ORDER BY stock ASC
        LIMIT 5
    """)


    for producto in cursor.fetchall():

        notificaciones.append({

            "icono":"⚠️",

            "mensaje":
            f"Stock bajo: {producto[0]} ({producto[1]} unidades)",

            "tipo":"warning"

        })




    # AGOTADOS

    cursor.execute("""
        SELECT nombre
        FROM productos
        WHERE stock = 0
        LIMIT 5
    """)



    for producto in cursor.fetchall():

        notificaciones.append({

            "icono":"🚨",

            "mensaje":
            f"Producto agotado: {producto[0]}",

            "tipo":"danger"

        })





    # ÚLTIMA VENTA

    cursor.execute("""
        SELECT cliente,total
        FROM ventas
        ORDER BY id DESC
        LIMIT 1
    """)



    venta = cursor.fetchone()


    if venta:


        notificaciones.append({

            "icono":"🛒",

            "mensaje":
            f"Última venta registrada: ${venta[1]:,.0f}",

            "tipo":"success"

        })



    conexion.close()


    return notificaciones

# ==========================================
# VENTAS SEGÚN PERIODO
# ==========================================

def ventas_por_periodo(periodo):

    conexion = conectar()

    cursor = conexion.cursor()


    if periodo == "hoy":

        filtro = """
        DATE(fecha)=DATE('now')
        """


    elif periodo == "7":

        filtro = """
        fecha >= DATE('now','-6 day')
        """


    elif periodo == "anio":

        filtro = """
        strftime('%Y',fecha)=strftime('%Y','now')
        """


    else:

        filtro = """
        strftime('%Y-%m',fecha)=strftime('%Y-%m','now')
        """



    cursor.execute(f"""

        SELECT
            DATE(fecha),
            SUM(total)

        FROM ventas

        WHERE {filtro}

        GROUP BY DATE(fecha)

        ORDER BY DATE(fecha)

    """)



    datos = [
        list(x)
        for x in cursor.fetchall()
    ]


    conexion.close()


    return datos

# ==========================================
# OBTENER EMPRESA
# ==========================================

def lista_productos_agotados():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            nombre,
            stock

        FROM productos

        WHERE stock = 0

        ORDER BY nombre

        LIMIT 10

    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos



# ==========================================
# PRODUCTOS AGOTADOS LISTA
# ==========================================

def obtener_empresa():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            nombre,
            rut,
            giro,
            direccion,
            comuna,
            telefono,
            email,
            logo,
            moneda,
            iva

        FROM empresa

        LIMIT 1
    """)

    empresa = cursor.fetchone()

    conexion.close()

    return empresa