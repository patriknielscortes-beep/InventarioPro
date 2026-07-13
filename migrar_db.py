import sqlite3

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Obtener columnas existentes
cursor.execute("PRAGMA table_info(usuarios)")
columnas = [fila[1] for fila in cursor.fetchall()]

# Agregar columna estado si no existe
if "estado" not in columnas:

    cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN estado TEXT DEFAULT 'Activo'
    """)

    print("✔ Columna 'estado' agregada.")

else:

    print("✔ La columna 'estado' ya existe.")

conexion.commit()
conexion.close()