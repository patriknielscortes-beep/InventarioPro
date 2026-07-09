import sqlite3


DATABASE = "inventario.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion



# ==========================================
# LISTAR CATEGORIAS
# ==========================================

def listar_categorias():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM categorias
        ORDER BY id DESC
    """)

    categorias = cursor.fetchall()

    conexion.close()

    return categorias



# ==========================================
# CREAR CATEGORIA
# ==========================================

def crear_categoria(nombre, descripcion):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO categorias
        (
            nombre,
            descripcion
        )
        VALUES
        (?, ?)
    """,
    (
        nombre,
        descripcion
    ))

    conexion.commit()

    conexion.close()



# ==========================================
# BUSCAR CATEGORIA
# ==========================================

def buscar_categoria(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM categorias
        WHERE id = ?
    """,
    (id,))


    categoria = cursor.fetchone()

    conexion.close()

    return categoria



# ==========================================
# ELIMINAR CATEGORIA
# ==========================================

def eliminar_categoria(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM categorias
        WHERE id = ?
    """,
    (id,))


    conexion.commit()

    conexion.close()