import sqlite3

DATABASE = "inventario.db"


def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.row_factory = sqlite3.Row

    return conexion



def obtener_empresa():

    conexion = conectar()

    cursor = conexion.cursor()


    cursor.execute("""
        SELECT *
        FROM empresa
        LIMIT 1
    """)


    empresa = cursor.fetchone()


    conexion.close()


    return empresa