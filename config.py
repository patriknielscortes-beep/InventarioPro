import os

class Config:
    # Clave secreta de Flask
    SECRET_KEY = "InventarioPro2026"

    # Base de datos SQLite
    DATABASE = "inventario.db"

    # Carpeta donde se guardarán las imágenes de productos
    UPLOAD_FOLDER = os.path.join("static", "uploads")

    # Tamaño máximo de archivo (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Extensiones permitidas para imágenes
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}