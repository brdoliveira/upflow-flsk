from tools.extractors.extraction_strategy import ExtractionStrategy

class PDFDataExtractor:
    """
    Classe para extração de dados de documentos PDF usando uma estratégia de extração específica.

    Atributos:
    -----------
    strategy : ExtractionStrategy
        Instância de uma estratégia de extração que implementa o método `extract_data`.
    
    Métodos:
    --------
    extract(text):
        Extrai os dados do texto fornecido utilizando a estratégia definida.
    """

    def __init__(self, strategy: ExtractionStrategy):
        """
        Inicializa a classe PDFDataExtractor com uma estratégia de extração específica.

        Parâmetros:
        -----------
        strategy : ExtractionStrategy
            Uma instância de uma classe que implementa a interface `ExtractionStrategy`.
        """
        self.strategy = strategy  # Recebe a estratégia a ser utilizada.

    def extract(self, text):
        """
        Extrai os dados do texto fornecido utilizando a estratégia definida.

        Parâmetros:
        -----------
        text : str
            O texto extraído de um documento PDF.

        Retorna:
        --------
        dict
            Um dicionário contendo os dados extraídos do texto.
        """
        return self.strategy.extract_data(text)  # Usa a estratégia para extrair os dados.
