import os

SECRET_KEY = 'flaskDbUpflow'
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'db_upflow'
    )
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/uploads/file"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024