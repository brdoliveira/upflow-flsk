from functools import wraps
from flask import redirect, url_for, session, flash
from enums import PermissionLevel

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(required_permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_permission = session.get('permission_level_id')
            if user_permission is None or user_permission > required_permission.value:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator