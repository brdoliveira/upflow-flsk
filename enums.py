from enum import Enum

class PermissionLevel(Enum):
    """
    Enumeração para representar os níveis de permissão dos usuários.
    
    Atributos:
    - ADMIN: Nível de permissão de administrador (valor 1).
    - EDITOR: Nível de permissão de editor (valor 2).
    - VIEWER: Nível de permissão de visualizador (valor 3).
    - GUEST: Nível de permissão de convidado (valor 4).
    """
    ADMIN = 1
    EDITOR = 2
    VIEWER = 3
    GUEST = 4