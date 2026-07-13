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
# TABLA MARCAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT DEFAULT 'Activo'
)
""")

# ==========================================
# TABLA PRODUCTOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    marca_id INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    precio REAL DEFAULT 0,
    sku TEXT UNIQUE,
    estado TEXT DEFAULT 'Activo',
    imagen TEXT,

    FOREIGN KEY(categoria_id)
        REFERENCES categorias(id),

    FOREIGN KEY(marca_id)
        REFERENCES marcas(id)
)
""")

# ==========================================
# TABLA MOVIMIENTOS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto_id INTEGER NOT NULL,

    tipo TEXT NOT NULL,

    cantidad INTEGER NOT NULL,

    fecha TEXT NOT NULL,

    usuario TEXT,

    FOREIGN KEY(producto_id)
        REFERENCES productos(id)

)
""")

# ==========================================
# TABLA PROVEEDORES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS proveedores (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    rut TEXT,

    telefono TEXT,

    email TEXT,

    direccion TEXT,

    estado TEXT DEFAULT 'Activo'

)
""")

# ==========================================
# TABLA COMPRAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS compras (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    proveedor_id INTEGER NOT NULL,

    fecha TEXT NOT NULL,

    total REAL DEFAULT 0,

    usuario TEXT,

    FOREIGN KEY(proveedor_id)
        REFERENCES proveedores(id)

)
""")

# ==========================================
# TABLA DETALLE COMPRAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_compras (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    compra_id INTEGER NOT NULL,

    producto_id INTEGER NOT NULL,

    cantidad INTEGER NOT NULL,

    precio REAL NOT NULL,

    subtotal REAL NOT NULL,

    FOREIGN KEY(compra_id)
        REFERENCES compras(id),

    FOREIGN KEY(producto_id)
        REFERENCES productos(id)

)
""")

# ==========================================
# TABLA CARRITO COMPRAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito_compras (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto_id INTEGER NOT NULL,

    cantidad INTEGER NOT NULL,

    precio REAL NOT NULL,

    subtotal REAL NOT NULL,

    usuario TEXT,

    FOREIGN KEY(producto_id)
        REFERENCES productos(id)

)
""")

# ==========================================
# TABLA VENTAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente TEXT,

    fecha TEXT NOT NULL,

    total REAL DEFAULT 0,

    usuario TEXT NOT NULL

)
""")

# ==========================================
# TABLA DETALLE VENTAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_ventas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    venta_id INTEGER NOT NULL,

    producto_id INTEGER NOT NULL,

    cantidad INTEGER NOT NULL,

    precio REAL NOT NULL,

    subtotal REAL NOT NULL,

    FOREIGN KEY(venta_id)
        REFERENCES ventas(id),

    FOREIGN KEY(producto_id)
        REFERENCES productos(id)

)
""")

# ==========================================
# TABLA CARRITO VENTAS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito_ventas (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto_id INTEGER NOT NULL,

    cantidad INTEGER NOT NULL,

    precio REAL NOT NULL,

    subtotal REAL NOT NULL,

    usuario TEXT,

    FOREIGN KEY(producto_id)
        REFERENCES productos(id)

)
""")

# ==========================================
# TABLA CLIENTES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    rut TEXT,

    telefono TEXT,

    email TEXT,

    direccion TEXT,

    estado TEXT DEFAULT 'Activo'

)
""")
# ==========================================
# CREAR USUARIO ADMINISTRADOR
# ==========================================

CREATE TABLE IF NOT EXISTS empresa (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    rut TEXT,

    giro TEXT,

    direccion TEXT,

    comuna TEXT,

    telefono TEXT,

    email TEXT

);
# ==========================================
# DATOS CHILENO
# ==========================================

CREATE TABLE IF NOT EXISTS empresa (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    rut TEXT,

    giro TEXT,

    direccion TEXT,

    comuna TEXT,

    telefono TEXT,

    email TEXT

);

cursor.execute("""
INSERT OR IGNORE INTO empresa
(
id,
nombre,
rut,# 
)
==========================================
# TABLA EMPRESA
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS empresa (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    rut TEXT,

    giro TEXT,

    direccion TEXT,

    comuna TEXT,

    telefono TEXT,

    email TEXT

)
""")


# ==========================================
# DATOS EMPRESA
# ==========================================

cursor.execute("""
INSERT OR IGNORE INTO empresa
(
    id,
    nombre,
    rut,
    giro,
    direccion,
    comuna,
    telefono,
    email
)
VALUES
(
    1,
    'InventarioPro',
    '76.123.456-7',
    'Sistema de Gestión Comercial',
    'Coquimbo',
    'Coquimbo',
    '+56 9 1234 5678',
    'contacto@inventariopro.cl'
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

print("✅ Base de datos configurada correctamente.")