from flask import Blueprint, render_template

from utils.helpers import login_required, role_required

from models.envio_correo_model import listar_envios


envios = Blueprint("envios", __name__)


# ==========================================
# HISTORIAL DE CORREOS
# ==========================================

@envios.route("/envios")
@login_required
@role_required("Administrador", "Vendedor")
def historial():

    datos = listar_envios()

    print("ENVÍOS:", datos)

    return render_template(
        "envios.html",
        envios=datos
    )
