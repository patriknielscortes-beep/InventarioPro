import sqlite3

conexion = sqlite3.connect("inventario.db")

cursor = conexion.cursor()


try:
    cursor.execute("""
        ALTER TABLE empresa 
        ADD COLUMN logo TEXT DEFAULT 'logo.png'
    """)
except:
    pass


try:
    cursor.execute("""
        ALTER TABLE empresa 
        ADD COLUMN moneda TEXT DEFAULT 'Peso Chileno'
    """)
except:
    pass


try:
    cursor.execute("""
        ALTER TABLE empresa 
        ADD COLUMN iva REAL DEFAULT 19
    """)
except:
    pass


conexion.commit()

conexion.close()


print("✅ Tabla empresa actualizada")