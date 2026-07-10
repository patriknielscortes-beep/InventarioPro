import sqlite3

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# LISTAR PROVEEDORES
# ==========================================

def listar_proveedores():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM proveedores
        ORDER BY id DESC
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos


# ==========================================
# CREAR PROVEEDOR
# ==========================================

def crear_proveedor(nombre, rut, telefono, email, direccion):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO proveedores
        (
            nombre,
            rut,
            telefono,
            email,
            direccion
        )
        VALUES
        (?, ?, ?, ?, ?)
    """,
    (
        nombre,
        rut,
        telefono,
        email,
        direccion
    ))

    conexion.commit()
    conexion.close()


# ==========================================
# BUSCAR PROVEEDOR
# ==========================================

def buscar_proveedor(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM proveedores
        WHERE id = ?
    """, (id,))

    proveedor = cursor.fetchone()

    conexion.close()

    return proveedor


# ==========================================
# EDITAR PROVEEDOR
# ==========================================

def editar_proveedor(id, nombre, rut, telefono, email, direccion):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE proveedores
        SET
            nombre = ?,
            rut = ?,
            telefono = ?,
            email = ?,
            direccion = ?
        WHERE id = ?
    """,
    (
        nombre,
        rut,
        telefono,
        email,
        direccion,
        id
    ))

    conexion.commit()
    conexion.close()


# ==========================================
# ELIMINAR PROVEEDOR
# ==========================================

def eliminar_proveedor(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()