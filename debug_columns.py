"""Parser com detecção de colunas por posição X"""
import fitz
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

# Página 2 - Hortencia
print("=" * 80)
print("PÁGINA 2 - HORTENCIA - ANÁLISE POR POSIÇÃO X")
print("=" * 80)

page = doc[1]

# Extrair textos com suas posições
blocks = page.get_text("dict")["blocks"]

# Coletar cabeçalhos dos dias e suas posições X
day_headers = {}
activity_keywords = ['organização', 'teste', 'formação', 'elaboração', 'relatório', 
                    'vistoria', 'suporte', 'reunião', 'atendimento', 'auditoria',
                    'levantamento', 'weekly', 'abertura', 'fechamento', 'controle']

for block in blocks:
    if block['type'] == 0:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]  # Posição X
                y = span['bbox'][1]  # Posição Y
                
                # Detectar cabeçalhos dos dias
                if 'Segunda-feira' in text or '15/06' in text:
                    day_headers['Segunda'] = x
                    print(f"Segunda-feira encontrada em X={x:.1f}")
                elif 'Terça-feira' in text or 'Terca-feira' in text or '16/06' in text:
                    day_headers['Terça'] = x
                    print(f"Terça-feira encontrada em X={x:.1f}")
                elif 'Quarta-feira' in text or '17/06' in text:
                    day_headers['Quarta'] = x
                    print(f"Quarta-feira encontrada em X={x:.1f}")
                elif 'Quinta-feira' in text or '18/06' in text:
                    day_headers['Quinta'] = x
                    print(f"Quinta-feira encontrada em X={x:.1f}")
                elif 'Sexta-feira' in text or '19/06' in text:
                    day_headers['Sexta'] = x
                    print(f"Sexta-feira encontrada em X={x:.1f}")

# Definir ranges de X para cada dia (com margem de tolerância)
print("\n" + "=" * 80)
print("RANGES DAS COLUNAS:")
print("=" * 80)

sorted_days = sorted(day_headers.items(), key=lambda x: x[1])
day_ranges = {}

for i, (day, x_pos) in enumerate(sorted_days):
    if i < len(sorted_days) - 1:
        next_x = sorted_days[i + 1][1]
        x_min = x_pos - 10
        x_max = (x_pos + next_x) / 2
    else:
        x_min = x_pos - 10
        x_max = 1000  # Margem final
    
    day_ranges[day] = (x_min, x_max)
    print(f"{day}: X entre {x_min:.1f} e {x_max:.1f}")

# Agora extrair atividades e classificar por posição X
activities_by_day = defaultdict(list)

print("\n" + "=" * 80)
print("ATIVIDADES POR DIA:")
print("=" * 80)

for block in blocks:
    if block['type'] == 0:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                
                # Verificar se é atividade
                text_lower = text.lower()
                if (any(kw in text_lower for kw in activity_keywords) and 
                    10 < len(text) < 200):
                    
                    # Determinar a qual dia pertence pela posição X
                    for day, (x_min, x_max) in day_ranges.items():
                        if x_min <= x <= x_max:
                            if text not in activities_by_day[day]:
                                activities_by_day[day].append(text)
                                print(f"[{day}] X={x:.1f}: {text[:60]}")
                            break

print("\n" + "=" * 80)
print("RESUMO:")
print("=" * 80)
for day in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']:
    count = len(activities_by_day[day])
    print(f"{day}: {count} atividades")

doc.close()
