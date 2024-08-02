from functools import wraps
from flask import redirect, url_for, session, flash
from enums import PermissionLevel

def login_required(f):
    """
    Decorador para verificar se o usuário está logado antes de acessar uma rota.

    Se o usuário não estiver logado, redireciona para a página de login e exibe uma mensagem de aviso.
    
    Parâmetros:
    - f: Função a ser decorada.
    
    Retorna:
    - Função decorada que verifica a autenticação do usuário.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(required_permission):
    """
    Decorador para verificar se o usuário tem a permissão necessária para acessar uma rota.

    Se o usuário não tiver a permissão necessária, redireciona para a página inicial e exibe uma mensagem de aviso.
    
    Parâmetros:
    - required_permission: Nível de permissão necessário para acessar a rota.
    
    Retorna:
    - Decorador que verifica o nível de permissão do usuário.
    """
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
