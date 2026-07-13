import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "inventario.db"


conexion = sqlite3.connect(DATABASE)

cursor = conexion.cursor()


nueva_password = generate_password_hash("admin123")


cursor.execute("""
UPDATE usuarios
SET password = ?
WHERE usuario = 'admin'
""",
(
    nueva_password,
))


conexion.commit()

conexion.close()


print("Administrador actualizado correctamente")
print("Usuario: admin")
print("Clave: admin123")