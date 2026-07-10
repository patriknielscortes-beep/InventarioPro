from blueprints.productos import productos
from flask import Flask
from config import Config
from blueprints.auth import auth
from blueprints.dashboard import dashboard
from blueprints.categorias import categorias
from blueprints.marcas import marcas
from blueprints.movimientos import movimientos
from blueprints.proveedores import proveedores
from blueprints.compras import compras


app = Flask(__name__)

app.config.from_object(Config)


# Registrar módulos
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(categorias)
app.register_blueprint(marcas)
app.register_blueprint(productos)
app.register_blueprint(movimientos)
app.register_blueprint(proveedores)
app.register_blueprint(compras)


if __name__ == "__main__":
    app.run(debug=True)