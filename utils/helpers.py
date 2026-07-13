from functools import wraps
from flask import session, redirect


# ==========================================
# VALIDAR LOGIN
# ==========================================

def login_required(func):

    @wraps(func)
    def verificar(*args, **kwargs):

        if "usuario" not in session:

            return redirect("/")

        return func(*args, **kwargs)

    return verificar



# ==========================================
# VALIDAR ROL
# ==========================================

def role_required(*roles):

    def decorador(func):

        @wraps(func)
        def verificar(*args, **kwargs):

            if "rol" not in session:

                return redirect("/")


            if session["rol"] not in roles:

                return redirect("/dashboard")


            return func(*args, **kwargs)


        return verificar


    return decorador