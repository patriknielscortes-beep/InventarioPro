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

def crear_producto(nombre, categoria_id, marca_id, stock, precio):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        INSERT INTO productos
        (
            nombre,
            categoria_id,
            marca_id,
            stock,
            precio
        )
        VALUES
        (?, ?, ?, ?, ?)
    """,
    (
        nombre,
        categoria_id,
        marca_id,
        stock,
        precio
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