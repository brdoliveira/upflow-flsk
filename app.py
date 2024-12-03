import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tools.pdf_classifier import PDFClassifier

path_abs = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
pdf_classifier = PDFClassifier()
pdf_classifier.load_dataset(f"{path_abs}/uploads/ml_files/")
pdf_classifier.train()

from views.views import *
from views.views_companies import *
from views.views_users import *
from views.views_files import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)