from tools.extractors.extraction_strategy import ExtractionStrategy

class PDFDataExtractor:
    def __init__(self, strategy: ExtractionStrategy):
        self.strategy = strategy  # Recebe a estratégia a ser utilizada.

    def extract(self, text):
        return self.strategy.extract_data(text)  # Usa a estratégia para extrair os dados.
