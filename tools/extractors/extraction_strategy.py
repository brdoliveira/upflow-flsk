from abc import ABC, abstractmethod

class ExtractionStrategy(ABC):
    """
    Classe abstrata para definir a interface de estratégias de extração de dados de textos de documentos PDF.

    Esta classe serve como base para todas as estratégias de extração de dados, garantindo que todas as subclasses implementem
    o método `extract_data`.

    Métodos Abstratos:
    ------------------
    extract_data(text):
        Método abstrato que deve ser implementado por qualquer classe que herde de `ExtractionStrategy`.
        Este método será responsável por extrair dados específicos do texto fornecido.
    """

    @abstractmethod
    def extract_data(self, text):
        """
        Extrai dados do texto fornecido.

        Este método deve ser implementado por subclasses que definem uma estratégia específica de extração.

        Parâmetros:
        -----------
        text : str
            O texto extraído de um documento PDF.

        Retorna:
        --------
        dict
            Um dicionário contendo os dados extraídos do texto.

        Observação:
        -----------
        Como este é um método abstrato, ele não contém implementação. Deve ser obrigatoriamente implementado nas subclasses.
        """
        pass
