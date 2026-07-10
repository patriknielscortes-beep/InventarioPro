import sqlite3


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
        SELECT 
            productos.*,
            categorias.nombre AS categoria,
            marcas.nombre AS marca

        FROM productos

        LEFT JOIN categorias
        ON productos.categoria_id = categorias.id

        LEFT JOIN marcas
        ON productos.marca_id = marcas.id

        ORDER BY productos.id DESC
    """)


    productos = cursor.fetchall()

    conexion.close()


    return productos



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

    conexion.close()

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