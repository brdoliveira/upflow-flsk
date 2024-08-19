from tools.extractors.extraction_strategy import ExtractionStrategy
import re

class BoletoExtractionStrategy(ExtractionStrategy):
    def extract_data(self, text):
        def extract_with_regex(pattern, text, default='', flags=0):
            match = re.search(pattern, text, flags)
            return match.group(1).strip() if match else default
        
        data = {
            'Cedente': {
                'Nome': extract_with_regex(r'Cedente\n(.*?)\nAgência/Código', text, flags=re.DOTALL),
                'Agência/Código': extract_with_regex(r'Agência/Código do Cedente\n([\d\s/]+)', text),
                'Espécie': extract_with_regex(r'Espécie\n(.*?)\n', text)
            },
            'Documento': {
                'Nosso Número': extract_with_regex(r'Nosso Número\n(\d+)', text),
                'Número do Documento': extract_with_regex(r'Número do Documento\n(\d+)', text),
                'CPF/CNPJ': extract_with_regex(r'CPF/CNPJ\n([\d./-]+)', text),
                'Vencimento': extract_with_regex(r'Vencimento\n([\d/]+)', text),
                'Valor do Documento': extract_with_regex(r'Valor do Documento\n([\d,.]+)', text).replace(',', '.')
            },
            'Descontos e Acréscimos': {
                'Desconto/Abatimento': extract_with_regex(r'\(-\) Desconto/Abatimento\n([\d,.]+)', text).replace(',', '.'),
                'Outras Deduções': extract_with_regex(r'\(-\) Outras Deduções\n([\d,.]+)', text).replace(',', '.'),
                'Mora/Multa': extract_with_regex(r'\(\+\) Mora/Multa\n([\d,.]+)', text).replace(',', '.'),
                'Outros Acréscimos': extract_with_regex(r'\(\+\) Outros Acréscimos\n([\d,.]+)', text).replace(',', '.'),
                'Valor Cobrado': extract_with_regex(r'\(=\) Valor Cobrado\n([\d,.]+)', text).replace(',', '.')
            },
            'Sacado': {
                'Nome': extract_with_regex(r'Sacado\n(.*?)\nAutenticação mecânica', text, flags=re.DOTALL),
                'Endereço': extract_with_regex(r'Endereço:\s*(.*?)(?:\n|$)', text, flags=re.DOTALL),
                'Bairro e CEP': extract_with_regex(r'Bairro, CEP: ([\d-]+)', text)
            },
            'Instruções': extract_with_regex(r'Instruções \(Texto de responsabilidade do Cedente\)\n(.*?)(?:\nSacado|$)', text, flags=re.DOTALL),
            'Autenticação Mecânica': extract_with_regex(r'Autenticação mecânica\n(.*?)(?:\n|$)', text, flags=re.DOTALL)
        }

        return data
