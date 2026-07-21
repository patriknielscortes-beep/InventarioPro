from flask import Blueprint, render_template, request, redirect
from utils.helpers import login_required, role_required

from models.usuario_admin_model import (
    listar_usuarios,
    buscar_usuario_id,
    crear_usuario,
    editar_usuario,
    eliminar_usuario,
    cambiar_password,
    cambiar_estado
)

usuarios = Blueprint("usuarios", __name__)


# ==========================================
# LISTAR USUARIOS
# ==========================================

@usuarios.route("/usuarios")
@login_required
@role_required("Administrador")
def lista():

    datos = listar_usuarios()

    return render_template(
        "usuarios.html",
        usuarios=datos
    )


# ==========================================
# NUEVO USUARIO
# ==========================================

@usuarios.route("/usuarios/nuevo")
@login_required
@role_required("Administrador")
def nuevo():

    return render_template("crear_usuario.html")


# ==========================================
# GUARDAR USUARIO
# ==========================================

@usuarios.route("/usuarios/guardar", methods=["POST"])
@login_required
@role_required("Administrador")
def guardar():

    crear_usuario(
        request.form["nombre"],
        request.form["usuario"],
        request.form["password"],
        request.form["rol"]
    )

    return redirect("/usuarios")


# ==========================================
# EDITAR USUARIO
# ==========================================

@usuarios.route("/usuarios/editar/<int:id>")
@login_required
@role_required("Administrador")
def editar(id):

    usuario = buscar_usuario_id(id)

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


# ==========================================
# ACTUALIZAR USUARIO
# ==========================================

@usuarios.route("/usuarios/actualizar/<int:id>", methods=["POST"])
@login_required
@role_required("Administrador")
def actualizar(id):

    editar_usuario(
        id,
        request.form["nombre"],
        request.form["usuario"],
        request.form["rol"]
    )

    return redirect("/usuarios")


# ==========================================
# CAMBIAR PASSWORD
# ==========================================

@usuarios.route("/usuarios/password/<int:id>", methods=["POST"])
@login_required
@role_required("Administrador")
def password(id):

    cambiar_password(
        id,
        request.form["password"]
    )

    return redirect("/usuarios")


# ==========================================
# CAMBIAR ESTADO
# ==========================================

@usuarios.route("/usuarios/estado/<int:id>")
@login_required
@role_required("Administrador")
def estado(id):

    usuario = buscar_usuario(id)

    if usuario["estado"] == "Activo":
        cambiar_estado(id, "Inactivo")
    else:
        cambiar_estado(id, "Activo")

    return redirect("/usuarios")


# ==========================================
# ELIMINAR USUARIO
# ==========================================

@usuarios.route("/usuarios/eliminar/<int:id>")
@login_required
@role_required("Administrador")
def eliminar(id):

    eliminar_usuario(id)

    return redirect("/usuarios")