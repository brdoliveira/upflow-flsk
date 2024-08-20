from tools.extractors.extraction_strategy import ExtractionStrategy
import re

class ImpostoDeRendaExtractionStrategy(ExtractionStrategy):
    def extract_data(self, text):
        def extract_with_regex(pattern, text, default='', flags=0):
            matches = re.findall(pattern, text, flags)
            return matches[0] if matches else default
        
            # Extrair dados do extrato do imposto de renda
        data = {
            'Dados do Contribuinte': {
                'Nome': extract_with_regex(r'Nome do Contribuinte:\s*(.*)', text),  # Extraindo após ":"
                'CPF': extract_with_regex(r'CPF:\s*(\d{3}\.\d{3}\.\d{3}-\d{2})', text),  # Apenas o CPF
                'Período Inicial': extract_with_regex(r'Período:\s*(\d{2}/\d{2}/\d{4})', text),  # Primeiro grupo de data
                'Período Final': extract_with_regex(r'Período:\s*\d{2}/\d{2}/\d{4}\s*-\s*(\d{2}/\d{2}/\d{4})', text)  # Data final após "-"
            },
            'Receitas': {
                'Tabela': extract_with_regex(r'Receitas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)  # Captura a seção de receitas
            },
            'Despesas': {
                'Tabela': extract_with_regex(r'Despesas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)  # Captura a seção de despesas
            },
            'Resumo': {
                'Total de Receitas': extract_with_regex(r'Total de Receitas:\s*R\$\s*([\d\.]+)', text),  # Apenas o valor após "R$"
                'Total de Despesas': extract_with_regex(r'Total de Despesas:\s*R\$\s*([\d\.]+)', text),  # Apenas o valor após "R$"
                'Imposto a Pagar': extract_with_regex(r'Imposto a Pagar:\s*R\$\s*([\d\.]+)', text)  # Apenas o valor após "R$"
            },
            'Nota': 'Extrato do Imposto de Renda' if 'Extrato do Imposto de Renda' in text else ''
        }

            # Separar as linhas de receitas
        receitas_section = extract_with_regex(r'Receitas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
        if receitas_section:
            data['Receitas']['Tabela'] = re.findall(r'(\d{2}/\d{2}/\d{4})\s+([^\d]+)\s+([\d\.]+)', receitas_section, flags=re.DOTALL)

        # Separar as linhas de despesas
        despesas_section = extract_with_regex(r'Despesas\s+Data\s+Descrição\s+Valor \(R\$\)\s*((?:\d{2}/\d{2}/\d{4}\s+[^\d]+\s+[\d\.]+\s*)+)', text, flags=re.DOTALL)
        if despesas_section:
            data['Despesas']['Tabela'] = re.findall(r'(\d{2}/\d{2}/\d{4})\s+([^\d]+)\s+([\d\.]+)', despesas_section, flags=re.DOTALL)

        return data
