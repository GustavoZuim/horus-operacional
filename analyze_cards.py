"""Analisar coordenadas dos blocos de texto no PDF"""
import fitz
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

# Página 2 - Hortencia
print("=" * 100)
print("PÁGINA 2 - HORTENCIA - ANÁLISE DE BLOCOS")
print("=" * 100)

page = doc[1]
blocks = page.get_text("dict")["blocks"]

# Primeiro, encontrar as colunas dos dias
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
print("ANÁLISE DOS CARDS (blocos que começam após os cabeçalhos dos dias)")
print("=" * 100)

# Detectar tipos de atividades (cabeçalhos de cards)
activity_types = [
    'Elaboração de Relatórios',
    'Organização Cadastral',
    'Vistoria à Unidade',
    'Teste de Funcionalidade',
    'Ação de Formação e Treinamento'
]

# Procurar blocos com esses cabeçalhos
card_count_by_column = defaultdict(list)
y_threshold_start = 200  # Após cabeçalhos dos dias (aproximado)

for block in blocks:
    if block['type'] == 0:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                y = span['bbox'][1]
                
                # Se é um cabeçalho de card e está após os cabeçalhos dos dias
                if y > y_threshold_start:
                    for act_type in activity_types:
                        if act_type in text:
                            # Determinar em qual coluna está
                            if 'Segunda' in day_positions and x < day_positions.get('Terça', 1000):
                                column = 'Segunda'
                            elif 'Terça' in day_positions and day_positions.get('Terça', 0) <= x < day_positions.get('Quarta', 1000):
                                column = 'Terça'
                            elif 'Quarta' in day_positions and day_positions.get('Quarta', 0) <= x < day_positions.get('Quinta', 1000):
                                column = 'Quarta'
                            elif 'Quinta' in day_positions and day_positions.get('Quinta', 0) <= x < day_positions.get('Sexta', 1000):
                                column = 'Quinta'
                            elif 'Sexta' in day_positions and x >= day_positions.get('Sexta', 0):
                                column = 'Sexta'
                            else:
                                column = 'Desconhecida'
                            
                            card_count_by_column[column].append({
                                'type': act_type,
                                'x': x,
                                'y': y,
                                'full_text': text
                            })
                            print(f"\n[{column}] X={x:.1f}, Y={y:.1f}")
                            print(f"  Tipo: {act_type}")
                            print(f"  Texto: {text[:100]}")

print("\n" + "=" * 100)
print("RESUMO DE CARDS POR COLUNA:")
print("=" * 100)
for day in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']:
    count = len(card_count_by_column[day])
    print(f"{day}: {count} cards")
    
doc.close()
