import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score
import os

class PDFClassifier:
    """
    Classe para classificação de documentos PDF utilizando aprendizado de máquina.

    Atributos:
    -----------
    vectorizer : CountVectorizer
        Vetorizador de texto para converter texto em uma matriz de contagem de tokens.
    model : MultinomialNB
        Modelo de classificação Naive Bayes Multinomial.
    paths : list
        Lista para armazenar os caminhos dos arquivos PDF.
    pdf_texts : list
        Lista para armazenar os textos processados extraídos dos PDFs.
    labels : list
        Lista para armazenar os rótulos (labels) associados aos PDFs.

    Métodos:
    --------
    extract_text_from_pdf(pdf_path):
        Extrai o texto de um arquivo PDF especificado.
    
    preprocess_text(text):
        Realiza o pré-processamento do texto extraído (remoção de caracteres especiais, números e conversão para minúsculas).
    
    load_pdfs(path, label):
        Carrega os PDFs de um diretório especificado, extrai e processa o texto, e associa um rótulo (label) a cada PDF.
    
    train_model():
        Treina o modelo de classificação utilizando os textos processados dos PDFs.
    
    evaluate_model(y_test, y_pred):
        Avalia o modelo utilizando métricas de desempenho como matriz de confusão, acurácia, F1-score e recall.
    
    predict_pdf_type(pdf_path):
        Prediz o tipo de documento PDF (Nota Fiscal, Boleto, Imposto de Renda) baseado no modelo treinado.
    """

    def __init__(self):
        """
        Inicializa a classe PDFClassifier com um vetor de contagem de palavras, um modelo Naive Bayes Multinomial
        e listas para armazenar os caminhos, textos processados e rótulos dos PDFs.
        """
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.paths = []
        self.pdf_texts = []
        self.labels = []

    def extract_text_from_pdf(self, pdf_path):
        """
        Extrai o texto de um arquivo PDF.

        Parâmetros:
        -----------
        pdf_path : str
            O caminho completo do arquivo PDF.

        Retorna:
        --------
        str
            O texto extraído do PDF.
        """
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def preprocess_text(self, text):
        """
        Realiza o pré-processamento do texto extraído do PDF.

        O pré-processamento inclui:
        - Remoção de caracteres especiais.
        - Remoção de números.
        - Conversão do texto para minúsculas.
        - Remoção de espaços extras.

        Parâmetros:
        -----------
        text : str
            O texto extraído do PDF.

        Retorna:
        --------
        str
            O texto processado.
        """
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\d', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def load_pdfs(self, path, label):
        """
        Carrega os arquivos PDF de um diretório especificado, extrai e processa o texto e associa um rótulo (label) a cada PDF.

        Parâmetros:
        -----------
        path : str
            O caminho do diretório que contém os arquivos PDF.
        label : int
            O rótulo associado aos PDFs (0: Boleto, 1: Nota Fiscal, 2: Imposto de Renda).

        Retorna:
        --------
        None
        """
        files = os.listdir(path)
        for file_name in files:
            pdf_path = os.path.join(path, file_name)
            self.paths.append(pdf_path)
            text = self.extract_text_from_pdf(pdf_path)
            preprocessed_text = self.preprocess_text(text)
            self.pdf_texts.append(preprocessed_text)
            self.labels.append(label)

    def train_model(self):
        """
        Treina o modelo de classificação Naive Bayes Multinomial com os textos processados dos PDFs.

        A função realiza a vetorização dos textos, divide os dados em conjuntos de treinamento e teste,
        e treina o modelo com o conjunto de treinamento. Após o treinamento, o modelo é avaliado com o conjunto de teste.

        Retorna:
        --------
        None
        """
        X = self.vectorizer.fit_transform(self.pdf_texts)
        X_train, X_test, y_train, y_test = train_test_split(X, self.labels, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        # Avaliação do modelo
        self.evaluate_model(y_test, y_pred)

    def evaluate_model(self, y_test, y_pred):
        """
        Avalia o modelo de classificação utilizando métricas como matriz de confusão, acurácia, F1-score e recall.

        Parâmetros:
        -----------
        y_test : list
            Os rótulos reais do conjunto de teste.
        y_pred : list
            Os rótulos preditos pelo modelo.

        Retorna:
        --------
        None
        """
        print("Matriz de Confusão:")
        conf_matrix = confusion_matrix(y_test, y_pred)
        print(conf_matrix)
        print(f'Acurácia: {accuracy_score(y_test, y_pred) * 100:.2f}%')
        print(f'F1-Score (macro): {f1_score(y_test, y_pred, average="macro"):.2f}')
        print(f'Recall (macro): {recall_score(y_test, y_pred, average="macro"):.2f}')

    def predict_pdf_type(self, pdf_path):
        """
        Prediz o tipo de documento PDF (Nota Fiscal, Boleto, Imposto de Renda) baseado no modelo treinado.

        Parâmetros:
        -----------
        pdf_path : str
            O caminho completo do arquivo PDF a ser classificado.

        Retorna:
        --------
        str
            O tipo de documento predito ("Nota Fiscal", "Boleto", "Imposto de Renda", ou "Tipo desconhecido").
        """
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
classifier.load_pdfs(r".\uploads\ml_files\imposto_de_renda", label=2)

# Carregar e processar PDFs de notas fiscais
classifier.load_pdfs(r".\uploads\ml_files\nota_fiscal", label=1)

# Carregar e processar PDFs de boletos
classifier.load_pdfs(r".\upflow-flsk\uploads\ml_files\boleto", label=0)

# Treinar o modelo
classifier.train_model()

# Fazer uma predição em um novo PDF
prediction = classifier.predict_pdf_type(r'.\uploads\ml_files\nota_fiscal\nota_fiscal_0.pdf')
print(prediction)
