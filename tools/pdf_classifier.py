import os
import PyPDF2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score

class PDFClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.model = MultinomialNB()
        self.pdf_texts = []
        self.labels = []
        self.confidence_threshold = 0.5  # Limiar de confiança para classificar

    def extract_text_from_pdf(self, pdf_path):
        """Extrai texto de um arquivo PDF."""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Erro ao processar o arquivo {pdf_path}: {e}")
            return ''

    def load_dataset(self, pdf_folder):
        """Carrega os PDFs e suas respectivas classes de um diretório."""
        texts = []
        labels = []
        for label in os.listdir(pdf_folder):
            label_path = os.path.join(pdf_folder, label)
            if os.path.isdir(label_path):
                for pdf_file in os.listdir(label_path):
                    if pdf_file.endswith('.pdf'):
                        pdf_path = os.path.join(label_path, pdf_file)
                        text = self.extract_text_from_pdf(pdf_path)
                        if text:
                            texts.append(text)
                            labels.append(label)
        self.pdf_texts = texts
        self.labels = labels

    def preprocess_text(self, text):
        """Pré-processa o texto para adequação ao modelo."""
        return text.lower()

    def tune_hyperparameters(self, plot_results=True):
        """Realiza a busca pelos melhores hiperparâmetros para o modelo Naive Bayes Multinomial."""
        X = self.vectorizer.fit_transform(self.pdf_texts)
        param_grid = {'alpha': [5.0]}
        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='f1_weighted', return_train_score=True)
        grid_search.fit(X, self.labels)
        
        # Salvar o melhor modelo
        self.model = grid_search.best_estimator_
        print(f'Melhores Hiperparâmetros: {grid_search.best_params_}')

        # Plotar resultados dos hiperparâmetros
        if plot_results:
            self.plot_alpha_results(grid_search, param_grid['alpha'])

        return grid_search.best_params_

    def plot_alpha_results(self, grid_search, alphas):
        """Plota o desempenho do modelo para diferentes valores de alpha com valores reais no eixo x."""
        mean_test_scores = grid_search.cv_results_['mean_test_score']

        plt.figure(figsize=(8, 5))
        plt.plot(alphas, mean_test_scores, marker='o', linestyle='-', label='F1-Score (média)')
        plt.xlabel('Valor de Alpha')
        plt.ylabel('F1-Score Médio')
        plt.title('Impacto de Alpha no Desempenho do Modelo')
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.xticks(alphas)  # Garante que todos os valores de alpha sejam mostrados no eixo x
        plt.legend()
        plt.tight_layout()
        plt.show()

    def train(self):
        """Treina o modelo com os dados carregados."""
        X = self.vectorizer.fit_transform(self.pdf_texts)
        y = np.array(self.labels)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        self.plot_metrics(y_test, y_pred)

    def predict_pdf_type(self, pdf_path):
        """Prediz o tipo de documento PDF baseado no modelo treinado."""
        text = self.extract_text_from_pdf(pdf_path)
        preprocessed_text = self.preprocess_text(text)
        vectorized_text = self.vectorizer.transform([preprocessed_text])

        # Obter as probabilidades de predição
        probabilities = self.model.predict_proba(vectorized_text)
        max_prob = np.max(probabilities)

        if max_prob < self.confidence_threshold:
            raise ValueError("Tipo de documento não reconhecido com confiança suficiente.")

        prediction = self.model.predict(vectorized_text)[0]
        return prediction

    def plot_metrics(self, y_test, y_pred):
        """Plota a matriz de confusão e exibe métricas de desempenho."""
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y_test), yticklabels=np.unique(y_test))
        plt.xlabel('Predito')
        plt.ylabel('Verdadeiro')
        plt.title('Matriz de Confusão')
        plt.show()

        print("Relatório de Classificação:")
        print(classification_report(y_test, y_pred))
        print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")
        print(f"F1-Score (média ponderada): {f1_score(y_test, y_pred, average='weighted'):.2f}")


if __name__ == "__main__":
    # Exemplo de uso da classe
    classifier = PDFClassifier()

    classifier.load_dataset(r"./uploads/ml_files/Files")

    # Ajustar hiperparâmetros (opcional)
    classifier.tune_hyperparameters()

    # Treinar o modelo
    classifier.train()

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
