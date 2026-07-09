import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "inventario.db"


conexion = sqlite3.connect(DATABASE)

cursor = conexion.cursor()


# ==========================================
# TABLA USUARIOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL,
    foto TEXT DEFAULT 'default.png'
)
""")


# ==========================================
# TABLA CATEGORIAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT DEFAULT 'Activo'
)
""")


# ==========================================
# CREAR USUARIO ADMINISTRADOR
# ==========================================

password = generate_password_hash("admin123")


cursor.execute("""
INSERT OR IGNORE INTO usuarios
(
    nombre,
    usuario,
    password,
    rol
)
VALUES
(
    'Administrador',
    'admin',
    ?,
    'Administrador'
)
""", (password,))


conexion.commit()

conexion.close()


print("Base de datos configurada correctamente.")