import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tools.pdf_classifier import PDFClassifier

path_abs = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
pdf_classifier = PDFClassifier()
pdf_classifier.load_pdfs(f"{path_abs}/uploads/ml_files/imposto_de_renda", label=2)
pdf_classifier.load_pdfs(f"{path_abs}/uploads/ml_files/nota_fiscal", label=1)
pdf_classifier.load_pdfs(f"{path_abs}/uploads/ml_files/boleto", label=0)
pdf_classifier.train_model()

from views.views import *
from views.views_companies import *
from views.views_users import *
from views.views_files import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)