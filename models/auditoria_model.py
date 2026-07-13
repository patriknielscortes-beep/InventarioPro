import sqlite3

DATABASE = "inventario.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


# ==========================================
# REGISTRAR AUDITORÍA
# ==========================================

def registrar_auditoria(usuario, modulo, accion):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO auditoria
        (
            usuario,
            modulo,
            accion
        )
        VALUES (?, ?, ?)
    """, (
        usuario,
        modulo,
        accion
    ))

    conexion.commit()
    conexion.close()


# ==========================================
# LISTAR AUDITORÍA
# ==========================================

def listar_auditoria():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM auditoria
        ORDER BY id DESC
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos