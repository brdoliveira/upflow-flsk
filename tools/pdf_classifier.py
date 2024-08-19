import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score
import os

class PDFClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.paths = []
        self.pdf_texts = []
        self.labels = []

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def preprocess_text(self, text):
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\d', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def load_pdfs(self, path, label):
        files = os.listdir(path)
        for file_name in files:
            pdf_path = os.path.join(path, file_name)
            self.paths.append(pdf_path)
            text = self.extract_text_from_pdf(pdf_path)
            preprocessed_text = self.preprocess_text(text)
            self.pdf_texts.append(preprocessed_text)
            self.labels.append(label)

    def train_model(self):
        X = self.vectorizer.fit_transform(self.pdf_texts)
        X_train, X_test, y_train, y_test = train_test_split(X, self.labels, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        # Avaliação do modelo
        self.evaluate_model(y_test, y_pred)

    def evaluate_model(self, y_test, y_pred):
        print("Matriz de Confusão:")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)
        print(f'Acurácia: {accuracy_score(y_test, y_pred) * 100:.2f}%')
        print(f'F1-Score (macro): {f1_score(y_test, y_pred, average="macro"):.2f}')
        print(f'Recall (macro): {recall_score(y_test, y_pred, average="macro"):.2f}')

    def predict_pdf_type(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        preprocessed_text = self.preprocess_text(text)
        vectorized_text = self.vectorizer.transform([preprocessed_text])
        prediction = self.model.predict(vectorized_text)[0]
        
        if prediction == 1:
            return "Nota Fiscal"
        elif prediction == 0:
            return "Boleto"
        elif prediction == 2:
            return "Imposto de Renda"
        else:
            return "Tipo desconhecido"

# Exemplo de uso da classe
classifier = PDFClassifier()

# Carregar e processar PDFs de imposto de renda
classifier.load_pdfs(r"C:\Users\brufe\OneDrive\Área de Trabalho\Git\upflow-flsk\uploads\ml_files\imposto_de_renda", label=2)

# Carregar e processar PDFs de notas fiscais
classifier.load_pdfs(r"C:\Users\brufe\OneDrive\Área de Trabalho\Git\upflow-flsk\uploads\ml_files\nota_fiscal", label=1)

# Carregar e processar PDFs de boletos
classifier.load_pdfs(r"C:\Users\brufe\OneDrive\Área de Trabalho\Git\upflow-flsk\uploads\ml_files\boleto", label=0)

# Treinar o modelo
classifier.train_model()

# Fazer uma predição em um novo PDF
prediction = classifier.predict_pdf_type(r'C:\Users\brufe\OneDrive\Área de Trabalho\Git\upflow-flsk\uploads\ml_files\nota_fiscal\nota_fiscal_0.pdf')
print(prediction)
