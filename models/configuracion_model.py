import sqlite3


DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



# ==========================================
# OBTENER DATOS EMPRESA
# ==========================================

def obtener_empresa():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM empresa
        WHERE id = 1
    """)


    empresa = cursor.fetchone()


    conexion.close()


    return empresa



# ==========================================
# ACTUALIZAR EMPRESA
# ==========================================

def actualizar_empresa(
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
):

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        UPDATE empresa
        SET

            nombre = ?,

            rut = ?,

            giro = ?,

            direccion = ?,

            comuna = ?,

            telefono = ?,

            email = ?,

            logo = ?,

            moneda = ?,

            iva = ?

        WHERE id = 1

    """,
    (
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
    ))


    conexion.commit()

    conexion.close()