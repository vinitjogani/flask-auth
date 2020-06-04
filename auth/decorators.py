from flask import request, redirect
from .models import User


def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        user = User.from_token(token)
        if user is not None:
            return func(user=user, *args, **kwargs)
        else:
            return redirect("/auth/login?next=" + request.path)
    return wrapper


def login_forbidden(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        user = User.from_token(token)
        if user is not None:
            return redirect("/")
        else:
            return func(*args, **kwargs)
    return wrapper
