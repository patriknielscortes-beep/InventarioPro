from functools import wraps
from flask import session, redirect


def login_required(func):

    @wraps(func)
    def verificar(*args, **kwargs):

        if "usuario" not in session:
            return redirect("/")

        return func(*args, **kwargs)

    return verificar