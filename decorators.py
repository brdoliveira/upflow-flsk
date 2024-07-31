from functools import wraps
from flask import redirect, url_for, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function