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
# BUSCAR CLIENTE POR NOMBRE
# ==========================================

def buscar_cliente_nombre(nombre):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE nombre = ?
        LIMIT 1
    """,
    (nombre,))


    cliente = cursor.fetchone()


    conexion.close()


    return cliente


# ==========================================
# EDITAR CLIENTE
# ==========================================

def editar_cliente(id, nombre, rut, telefono, email, direccion):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        UPDATE clientes
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
# BUSCAR CLIENTE POR EMAIL
# ==========================================

def buscar_email(email):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE email = ?
    """,
    (email,))


    cliente = cursor.fetchone()


    conexion.close()


    return cliente

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

    # ==========================================
# BUSCAR CLIENTE POR ID
# ==========================================

def obtener_cliente(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = ?
    """,
    (id,))


    cliente = cursor.fetchone()


    conexion.close()


    return cliente



# ==========================================
# HISTORIAL DE COMPRAS DEL CLIENTE
# ==========================================

def historial_cliente(cliente):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT
            id,
            folio,
            total,
            fecha,
            forma_pago

        FROM ventas

        WHERE cliente = ?

        ORDER BY id DESC

    """,
    (cliente,))


    ventas = cursor.fetchall()


    conexion.close()


    return ventas



# ==========================================
# RESUMEN DE COMPRAS DEL CLIENTE
# ==========================================

def resumen_cliente(cliente):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT

            COUNT(id),
            COALESCE(SUM(total),0)

        FROM ventas

        WHERE cliente = ?

    """,
    (cliente,))


    datos = cursor.fetchone()


    conexion.close()


    return datos

# ==========================================
# VALIDAR RUT EXISTENTE
# ==========================================

def buscar_rut(rut):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE rut = ?
    """,
    (rut,))


    cliente = cursor.fetchone()

    conexion.close()


    return cliente



# ==========================================
# VALIDAR EMAIL EXISTENTE
# ==========================================

def buscar_email(email):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE email = ?
    """,
    (email,))


    cliente = cursor.fetchone()

    conexion.close()


    return cliente