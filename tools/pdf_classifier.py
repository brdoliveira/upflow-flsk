import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score, classification_report
import os
import pickle
import json
import seaborn as sns
import matplotlib.pyplot as plt

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
    
    tune_hyperparameters():
        Ajusta os hiperparâmetros do modelo para melhorar a performance.
    
    save_model(model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        Salva o modelo treinado e o vetorizador em arquivos.
    
    load_model(model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        Carrega o modelo treinado e o vetorizador a partir de arquivos.
    
    log_performance(log_path='model_performance.json', accuracy=None, f1=None, recall=None):
        Registra a performance do modelo em um arquivo JSON.
    
    plot_confusion_matrix(y_test, y_pred):
        Gera uma visualização gráfica da matriz de confusão.
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
        self.plot_confusion_matrix(y_test, y_pred)
        self.log_performance(accuracy=accuracy_score(y_test, y_pred), 
                             f1=f1_score(y_test, y_pred, average="macro"), 
                             recall=recall_score(y_test, y_pred, average="macro"))

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

    def tune_hyperparameters(self):
        """
        Realiza a busca pelos melhores hiperparâmetros para o modelo Naive Bayes Multinomial.

        Retorna:
        --------
        dict
            Os melhores hiperparâmetros encontrados.
        """
        # Ajustar o vectorizer antes de procurar os melhores hiperparâmetros
        X = self.vectorizer.fit_transform(self.pdf_texts)
        
        param_grid = {'alpha': [0.1, 0.5, 1.0, 5.0, 10.0]}
        grid_search = GridSearchCV(self.model, param_grid, cv=5)
        
        # Realizar o ajuste com os dados vetorizados
        grid_search.fit(X, self.labels)
        
        print(f'Melhores Hiperparâmetros: {grid_search.best_params_}')
        return grid_search.best_params_

    def save_model(self, model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        """
        Salva o modelo treinado e o vetorizador em arquivos.

        Parâmetros:
        -----------
        model_path : str
            Caminho para salvar o arquivo do modelo.
        vectorizer_path : str
            Caminho para salvar o arquivo do vetorizador.

        Retorna:
        --------
        None
        """
        with open(model_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)
        with open(vectorizer_path, 'wb') as vectorizer_file:
            pickle.dump(self.vectorizer, vectorizer_file)

    def load_model(self, model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
        """
        Carrega o modelo treinado e o vetorizador a partir de arquivos.

        Parâmetros:
        -----------
        model_path : str
            Caminho do arquivo do modelo salvo.
        vectorizer_path : str
            Caminho do arquivo do vetorizador salvo.

        Retorna:
        --------
        None
        """
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open(vectorizer_path, 'rb') as vectorizer_file:
            self.vectorizer = pickle.load(vectorizer_file)

    def log_performance(self, log_path='model_performance.json', accuracy=None, f1=None, recall=None):
        """
        Registra a performance do modelo em um arquivo JSON.

        Parâmetros:
        -----------
        log_path : str
            Caminho do arquivo de log de performance.
        accuracy : float
            Acurácia do modelo.
        f1 : float
            F1-Score do modelo.
        recall : float
            Recall do modelo.

        Retorna:
        --------
        None
        """
        performance_data = {
            'accuracy': accuracy,
            'f1_score': f1,
            'recall': recall
        }
        
        if os.path.exists(log_path):
            with open(log_path, 'r+') as file:
                data = json.load(file)
                data['performances'].append(performance_data)
                file.seek(0)
                json.dump(data, file)
        else:
            with open(log_path, 'w') as file:
                json.dump({'performances': [performance_data]}, file)

    def plot_confusion_matrix(self, y_test, y_pred):
        """
        Gera uma visualização gráfica da matriz de confusão.

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
        conf_matrix = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", 
                    xticklabels=['Boleto', 'Nota Fiscal', 'Imposto de Renda'], 
                    yticklabels=['Boleto', 'Nota Fiscal', 'Imposto de Renda'])
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Matriz de Confusão')
        plt.show()

if __name__ == "__main__":
    # Exemplo de uso da classe
    classifier = PDFClassifier()

    # Carregar e processar PDFs de imposto de renda
    classifier.load_pdfs(r"./uploads/ml_files/imposto_de_renda", label=2)

    # Carregar e processar PDFs de notas fiscais
    classifier.load_pdfs(r"./uploads/ml_files/nota_fiscal", label=1)

    # Carregar e processar PDFs de boletos
    classifier.load_pdfs(r"./uploads/ml_files/boleto", label=0)

    # Ajustar hiperparâmetros (opcional)
    classifier.tune_hyperparameters()

    # Treinar o modelo
    classifier.train_model()

    # Fazer uma predição em um novo PDF
    prediction = classifier.predict_pdf_type(r'./uploads/ml_files/nota_fiscal/nota_fiscal_0.pdf')
    print(f'Predição: {prediction}')

    # Salvar o modelo treinado e o vetorizador
    classifier.save_model(model_path='pdf_classifier_model.pkl', vectorizer_path='pdf_vectorizer.pkl')

    # Carregar o modelo e o vetorizador salvos
    classifier.load_model(model_path='pdf_classifier_model.pkl', vectorizer_path='pdf_vectorizer.pkl')

    # Fazer uma nova predição usando o modelo carregado
    new_prediction = classifier.predict_pdf_type(r'./uploads/ml_files/boleto/boleto_0d3c2b8d56554985be7d4a8f9dbd13fb.pdf')
    print(f'Nova Predição: {new_prediction}')