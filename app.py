from blueprints.productos import productos
from flask import Flask
from config import Config
from blueprints.auth import auth
from blueprints.dashboard import dashboard
from blueprints.categorias import categorias
from blueprints.marcas import marcas
from blueprints.movimientos import movimientos


app = Flask(__name__)

app.config.from_object(Config)


# Registrar módulos
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(categorias)
app.register_blueprint(marcas)
app.register_blueprint(productos)
app.register_blueprint(movimientos)


if __name__ == "__main__":
    app.run(debug=True)