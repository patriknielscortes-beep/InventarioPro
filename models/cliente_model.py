import sqlite3


DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# LISTAR CLIENTES
# ==========================================

def listar_clientes():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM clientes
        ORDER BY id DESC
    """)


    datos = cursor.fetchall()


    conexion.close()


    return datos



# ==========================================
# CREAR CLIENTE
# ==========================================

def crear_cliente(nombre, rut, telefono, email, direccion):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        INSERT INTO clientes
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
# ELIMINAR CLIENTE
# ==========================================

def eliminar_cliente(id):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        DELETE FROM clientes
        WHERE id = ?
    """,
    (id,))


    conexion.commit()

    conexion.close()