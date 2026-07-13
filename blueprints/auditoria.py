from flask import Blueprint, render_template

from utils.helpers import login_required, role_required
from models.auditoria_model import listar_auditoria

auditoria = Blueprint("auditoria", __name__)


# ==========================================
# AUDITORÍA
# ==========================================

@auditoria.route("/auditoria")
@login_required
@role_required("Administrador")
def lista():

    registros = listar_auditoria()

    return render_template(
        "auditoria.html",
        registros=registros
    )