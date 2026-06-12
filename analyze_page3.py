"""Analisar página 3 (continuação Hortencia)"""
import fitz
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

# Página 3 - Continuação Hortencia
print("=" * 100)
print("PÁGINA 3 - CONTINUAÇÃO HORTENCIA")
print("=" * 100)

page = doc[2]
blocks = page.get_text("dict")["blocks"]

# Encontrar as colunas dos dias
day_positions = {}
for block in blocks:
    if block['type'] == 0:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                y = span['bbox'][1]
                
                if 'Segunda-feira' in text:
                    day_positions['Segunda'] = x
                    print(f"Segunda-feira: X={x:.1f}, Y={y:.1f}")
                elif 'Terça-feira' in text or 'Terca-feira' in text:
                    day_positions['Terça'] = x
                    print(f"Terça-feira: X={x:.1f}, Y={y:.1f}")
                elif 'Quarta-feira' in text:
                    day_positions['Quarta'] = x
                    print(f"Quarta-feira: X={x:.1f}, Y={y:.1f}")
                elif 'Quinta-feira' in text:
                    day_positions['Quinta'] = x
                    print(f"Quinta-feira: X={x:.1f}, Y={y:.1f}")
                elif 'Sexta-feira' in text:
                    day_positions['Sexta'] = x
                    print(f"Sexta-feira: X={x:.1f}, Y={y:.1f}")

print("\n" + "=" * 100)
print("CARDS NA PÁGINA 3:")
print("=" * 100)

activity_types = [
    'Elaboração de Relatórios',
    'Organização Cadastral',
    'Vistoria à Unidade',
    'Teste de Funcionalidade',
    'Ação de Formação e Treinamento'
]

card_count_by_column = defaultdict(list)
y_threshold_start = 150  # Após cabeçalhos dos dias

for block in blocks:
    if block['type'] == 0:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                y = span['bbox'][1]
                
                if y > y_threshold_start:
                    for act_type in activity_types:
                        if act_type in text:
                            # Determinar coluna
                            if x < 150:
                                column = 'Segunda'
                            elif 150 <= x < 300:
                                column = 'Terça'
                            elif 300 <= x < 450:
                                column = 'Quarta'
                            elif 450 <= x < 650:
                                column = 'Quinta'
                            else:
                                column = 'Sexta'
                            
                            card_count_by_column[column].append({
                                'type': act_type,
                                'x': x,
                                'y': y
                            })
                            print(f"[{column}] X={x:.1f}, Y={y:.1f}: {act_type}")

print("\n" + "=" * 100)
print("RESUMO PÁGINA 3:")
print("=" * 100)
for day in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']:
    count = len(card_count_by_column[day])
    print(f"{day}: {count} cards")

doc.close()
