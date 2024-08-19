from tools.extractors.extraction_strategy import ExtractionStrategy
import re

class ImpostoDeRendaExtractionStrategy(ExtractionStrategy):
    def extract_data(self, text):
        def extract_with_regex(pattern, text, default='', flags=0):
            match = re.search(pattern, text, flags)
            return match.group(1).strip() if match else default
        
        # Extrair dados do extrato do imposto de renda
        data = {
            'Contribuinte': {
                'Nome': extract_with_regex(r'Nome do Contribuinte:\s*(.*?)\n', text),
                'CPF': extract_with_regex(r'CPF:\s*([\d.-]+)', text)
            },
            'Período': extract_with_regex(r'Período:\s*([\d/ -]+)', text),
            'Receitas': {
                'Data': re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', text),
                'Descrição': re.findall(r'\d{2}/\d{2}/\d{4}\s*(.*?)\s*[\d,.]+', text),
                'Valor': [float(v.replace(',', '.')) for v in re.findall(r'\d{2}/\d{2}/\d{4}\s*.*?\s*([\d,.]+)', text)]
            },
            'Despesas': {
                'Data': re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', text),
                'Descrição': re.findall(r'\d{2}/\d{2}/\d{4}\s*(.*?)\s*[\d,.]+', text),
                'Valor': [float(v.replace(',', '.')) for v in re.findall(r'\d{2}/\d{2}/\d{4}\s*.*?\s*([\d,.]+)', text)]
            },
            'Resumo': {
                'Total de Receitas': extract_with_regex(r'Total de Receitas:\s*R\$ ([\d,.]+)', text).replace(',', '.'),
                'Total de Despesas': extract_with_regex(r'Total de Despesas:\s*R\$ ([\d,.]+)', text).replace(',', '.'),
                'Imposto a Pagar': extract_with_regex(r'Imposto a Pagar:\s*R\$ ([\d,.]+)', text).replace(',', '.')
            }
        }

        return data
