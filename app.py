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
from blueprints.usuarios import usuarios
from blueprints.ventas import ventas
from blueprints.clientes import clientes
from blueprints.pos import pos
from blueprints.auditoria import auditoria
from blueprints.reportes import reportes
from blueprints.envios import envios



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
app.register_blueprint(usuarios)
app.register_blueprint(ventas)
app.register_blueprint(clientes)
app.register_blueprint(pos)
app.register_blueprint(auditoria)
app.register_blueprint(reportes)
app.register_blueprint(envios)



if __name__ == "__main__":
    app.run(debug=True)