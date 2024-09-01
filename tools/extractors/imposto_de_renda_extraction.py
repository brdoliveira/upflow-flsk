from tools.extractors.extraction_strategy import ExtractionStrategy
import re

class ImpostoDeRendaExtractionStrategy(ExtractionStrategy):
    def extract_data(self, text):
        def extract_with_regex(pattern, text, default='', flags=0):
            matches = re.findall(pattern, text, flags)
            return matches[0] if matches else default
        
        def format_decimal(value):
            try:
                return f"{float(value.replace('.', '').replace(',', '.')):.2f}"
            except ValueError:
                return value

        # Processamento do texto para garantir que está no formato correto
        text = text.encode('utf-8').decode('unicode_escape')

        # Extrair dados do extrato do imposto de renda
        data = {
            'Dados do Contribuinte': {
                'Nome': extract_with_regex(r'Nome do Contribuinte:\s*(.*)', text),
                'CPF': extract_with_regex(r'CPF:\s*(\d{3}\.\d{3}\.\d{3}-\d{2})', text),
                'Período Inicial': extract_with_regex(r'Período:\s*(\d{2}/\d{2}/\d{4})', text),
                'Período Final': extract_with_regex(r'Período:\s*\d{2}/\d{2}/\d{4}\s*-\s*(\d{2}/\d{2}/\d{4})', text)
            },
            'Receitas': {
                'Tabela': extract_with_regex(r'Receitas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
            },
            'Despesas': {
                'Tabela': extract_with_regex(r'Despesas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
            },
            'Resumo': {
                'Total de Receitas': format_decimal(extract_with_regex(r'Total de Receitas:\s*R\$\s*([\d\.]+)', text)),
                'Total de Despesas': format_decimal(extract_with_regex(r'Total de Despesas:\s*R\$\s*([\d\.]+)', text)),
                'Imposto a Pagar': format_decimal(extract_with_regex(r'Imposto a Pagar:\s*R\$\s*([\d\.]+)', text))
            },
            'Nota': 'Extrato do Imposto de Renda' if 'Extrato do Imposto de Renda' in text else ''
        }

        # Separar as linhas de receitas
        receitas_section = extract_with_regex(r'Receitas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
        if receitas_section:
            data['Receitas']['Tabela'] = [
                (date, description, format_decimal(value))
                for date, description, value in re.findall(r'(\d{2}/\d{2}/\d{4})\s+([^\d]+)\s+([\d\.]+)', receitas_section, flags=re.DOTALL)
            ]

        # Separar as linhas de despesas
        despesas_section = extract_with_regex(r'Despesas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
        if despesas_section:
            data['Despesas']['Tabela'] = [
                (date, description, format_decimal(value))
                for date, description, value in re.findall(r'(\d{2}/\d{2}/\d{4})\s+([^\d]+)\s+([\d\.]+)', despesas_section, flags=re.DOTALL)
            ]

        return data
