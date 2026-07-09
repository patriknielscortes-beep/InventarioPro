import sqlite3


DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR MARCAS
# ==========================================

def listar_marcas():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM marcas
        ORDER BY id DESC
    """)

    marcas = cursor.fetchall()

    conexion.close()

    return marcas



# ==========================================
# CREAR MARCA
# ==========================================

def crear_marca(nombre, descripcion):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO marcas
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
# BUSCAR MARCA
# ==========================================

def buscar_marca(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM marcas
        WHERE id = ?
    """,
    (id,))


    marca = cursor.fetchone()

    conexion.close()

    return marca



# ==========================================
# EDITAR MARCA
# ==========================================

def editar_marca(id, nombre, descripcion):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE marcas
        SET nombre = ?,
            descripcion = ?
        WHERE id = ?
    """,
    (
        nombre,
        descripcion,
        id
    ))


    conexion.commit()

    conexion.close()



# ==========================================
# ELIMINAR MARCA
# ==========================================

def eliminar_marca(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM marcas
        WHERE id = ?
    """,
    (id,))


    conexion.commit()

    conexion.close()