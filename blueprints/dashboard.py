from flask import Blueprint, render_template, session, redirect


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def inicio():

    if "usuario" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        rol=session["rol"]
    )