import sqlite3

conexion = sqlite3.connect("inventario.db")

cursor = conexion.cursor()


try:

    cursor.execute("""
        ALTER TABLE ventas
        ADD COLUMN neto REAL DEFAULT 0
    """)

    print("✅ Columna neto agregada")


except sqlite3.OperationalError:

    print("ℹ️ neto ya existe")



try:

    cursor.execute("""
        ALTER TABLE ventas
        ADD COLUMN iva REAL DEFAULT 0
    """)

    print("✅ Columna iva agregada")


except sqlite3.OperationalError:

    print("ℹ️ iva ya existe")



conexion.commit()

conexion.close()


print("✅ Actualización terminada")