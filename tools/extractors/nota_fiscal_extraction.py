from tools.extractors.extraction_strategy import ExtractionStrategy
import re

class NotaFiscalExtractionStrategy(ExtractionStrategy):
    def extract_data(self, text):
        def extract_with_regex(pattern, text, default='', flags=0):
            match = re.search(pattern, text, flags)
            return match.group(1).strip() if match else default

        def format_decimal(value):
            try:
                return f"{float(value.replace(',', '.')):.2f}"
            except ValueError:
                return value

        # Processamento do texto para garantir que está no formato correto
        text = text.encode('utf-8').decode('unicode_escape')

        data = {
            'Dados da Nota Fiscal': {
                'Numero da Nota Fiscal': extract_with_regex(r'NFe No (\d+)', text),
                'Serie': extract_with_regex(r'Série (\d+)', text),
                'Data de Emissao': extract_with_regex(r'Data de Emissão ([\d/ :]+)', text),
                'Modelo': extract_with_regex(r'Modelo\s*(\d{2} - NF-E EMITIDA EM SUBSTITUIÇÃO AO MODELO \d+\s*OU \d\w?)', text),
                'Natureza da Operacao': extract_with_regex(r'Natureza da\s*Operação\s*([^\n]+\s*[^\n]*)', text, flags=re.DOTALL),
                'Evento Mais Recente': extract_with_regex(r'Evento Mais\s*Recente\s*([^\n]+)', text, flags=re.DOTALL),
                'Data/Hora Evento Mais Recente': extract_with_regex(r'Data/Hora Evento Mais Recente\s+([\d/ :]+)', text),
                'Chave de Acesso': extract_with_regex(r'Chave de\s*Acesso\s*(\d{44})', text, flags=re.DOTALL)
            },
            'Dados do Emitente': {
                'CPF/CNPJ': extract_with_regex(r'CPF/CNPJ\s+(\d+)', text),
                'Razao Social': extract_with_regex(r'Razão Social\s+(.+?)\n', text, flags=re.DOTALL),
                'UF': extract_with_regex(r'UF\s+(\w+)', text),
                'Municipio': extract_with_regex(r'Município\s+([\w ]+)', text)
            },
            'Dados do Destinatario': {
                'CNPJ': extract_with_regex(r'CNPJ\s+(\d+)', text),
                'Nome': extract_with_regex(r'Nome\s*([A-Z\s,]+(?:\n[A-Z\s,]+)*)\n', text, flags=re.DOTALL),
                'UF': extract_with_regex(r'UF\s+(\w+)', text),
                'Indicador IE': extract_with_regex(r'Indicador IE\s+([\w ]+)', text),
                'Destino da Operacao': extract_with_regex(r'Destino da\s*Operação\s*([\d -]+[^\n]*)', text, flags=re.DOTALL),
                'Consumidor Final': extract_with_regex(r'Consumidor Final\s+(\d+ - \w+)', text),
                'Presenca do Comprador': extract_with_regex(r'Presença do\s*Comprador\s*([\d -]+[^\n]*)', text, flags=re.DOTALL)
            },
            'Valor Nota Fiscal': {
                'Valor': format_decimal(extract_with_regex(r'Valor Nota Fiscal\s+([\d,]+)', text))
            },
            'Nota': 'Nota Fiscal gerada automaticamente' if 'Nota Fiscal gerada automaticamente' in text else ''
        }

        return data
