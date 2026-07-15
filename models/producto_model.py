import sqlite3
import barcode
from barcode.writer import ImageWriter
import os

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR PRODUCTOS
# ==========================================

def listar_productos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM productos
        ORDER BY id DESC
    """)

    productos = cursor.fetchall()

    conexion.close()

    return productos


# ==========================================
# GENERAR CODIGO DE BARRAS
# ==========================================

def generar_codigo_barras(sku):

    carpeta = "static/barcodes"


    if not os.path.exists(carpeta):
        os.makedirs(carpeta)


    ruta = os.path.join(
        carpeta,
        sku
    )


    codigo = barcode.get(
        "code128",
        sku,
        writer=ImageWriter()
    )


    archivo = codigo.save(ruta)


    return archivo

# ==========================================
# CREAR PRODUCTO
# ==========================================

def crear_producto(nombre, categoria_id, marca_id, stock, precio, imagen):

    conexion = conectar()

    cursor = conexion.cursor()


    # Generar SKU automático

    cursor.execute("""
        SELECT COUNT(*) 
        FROM productos
    """)

    total = cursor.fetchone()[0] + 1


    sku = f"PROD-{total:05d}"


    cursor.execute("""
        INSERT INTO productos
        (
            nombre,
            categoria_id,
            marca_id,
            stock,
            precio,
            sku,
            imagen
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        nombre,
        categoria_id,
        marca_id,
        stock,
        precio,
        sku,
        imagen
    ))


    conexion.commit()

    generar_codigo_barras(sku)

    conexion.close()

    # ==========================================
# OBTENER PRODUCTO POR ID COMPLETO
# ==========================================

def obtener_producto(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id = ?
    """,
    (id,))


    producto = cursor.fetchone()


    conexion.close()


    return producto

# ==========================================
# BUSCAR PRODUCTO
# ==========================================

def buscar_producto(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id = ?
    """,
    (id,))

    producto = cursor.fetchone()

    conexion.close()

    return producto



# ==========================================
# EDITAR PRODUCTO
# ==========================================

def editar_producto(id, nombre, categoria_id, marca_id, stock, precio):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE productos
        SET nombre = ?,
            categoria_id = ?,
            marca_id = ?,
            stock = ?,
            precio = ?
        WHERE id = ?
    """,
    (
        nombre,
        categoria_id,
        marca_id,
        stock,
        precio,
        id
    ))

    conexion.commit()

    conexion.close()



# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id = ?
    """,
    (id,))


    conexion.commit()

    conexion.close()



# ==========================================
# BUSCAR PRODUCTOS
# ==========================================

def buscar_productos(texto):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            productos.*,
            categorias.nombre AS categoria,
            marcas.nombre AS marca

        FROM productos

        LEFT JOIN categorias
        ON productos.categoria_id = categorias.id

        LEFT JOIN marcas
        ON productos.marca_id = marcas.id

        WHERE productos.nombre LIKE ?
        OR categorias.nombre LIKE ?
        OR marcas.nombre LIKE ?

        ORDER BY productos.id DESC
    """,
    (
        "%" + texto + "%",
        "%" + texto + "%",
        "%" + texto + "%"
    ))

    productos = cursor.fetchall()

    conexion.close()

    return productos

# ==========================================
# BUSCAR POR SKU
# ==========================================

def buscar_por_sku(sku):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            productos.*,
            categorias.nombre AS categoria,
            marcas.nombre AS marca

        FROM productos

        LEFT JOIN categorias
        ON productos.categoria_id = categorias.id

        LEFT JOIN marcas
        ON productos.marca_id = marcas.id

        WHERE productos.sku = ?

    """,
    (sku,))


    producto = cursor.fetchone()


    conexion.close()


    return producto

# ==========================================
# DESCONTAR STOCK VENTA
# ==========================================

def actualizar_stock_venta(producto_id, cantidad):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, stock FROM productos WHERE id = ?",
        (producto_id,)
    )

    producto = cursor.fetchone()

    print("DESCONTANDO STOCK:")
    print("Producto:", producto["nombre"])
    print("Stock antes:", producto["stock"])
    print("Cantidad:", cantidad)

    cursor.execute("""
        UPDATE productos
        SET stock = stock - ?
        WHERE id = ?
    """,
    (
        cantidad,
        producto_id
    ))

    cursor.execute(
        "SELECT stock FROM productos WHERE id = ?",
        (producto_id,)
    )

    print("Stock después:", cursor.fetchone()["stock"])

    conexion.commit()
    conexion.close()

    
# ==========================================
# ACTUALIZAR STOCK POR COMPRA
# ==========================================

def actualizar_stock_compra(producto_id, cantidad):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE productos
        SET stock = stock + ?
        WHERE id = ?
    """,
    (
        cantidad,
        producto_id
    ))

    conexion.commit()

    conexion.close()