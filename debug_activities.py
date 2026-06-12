"""Debug para verificar extração de atividades por dia"""
import fitz
import re
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

# Processar página 2 (Hortencia)
print("=" * 80)
print("PÁGINA 2 - HORTENCIA")
print("=" * 80)

page = doc[1]  # Página 2 (índice 1)
page_text = page.get_text()

lines = [l.strip() for l in page_text.split('\n') if l.strip()]

# Detectar cabeçalhos dos dias
day_patterns = {
    'Segunda-feira': [r'Segunda-feira', r'Segunda\s+feira', r'15/06'],
    'Terça-feira': [r'Terça-feira', r'Terca-feira', r'Ter[çc]a\s+feira', r'16/06'],
    'Quarta-feira': [r'Quarta-feira', r'Quarta\s+feira', r'17/06'],
    'Quinta-feira': [r'Quinta-feira', r'Quinta\s+feira', r'18/06'],
    'Sexta-feira': [r'Sexta-feira', r'Sexta\s+feira', r'19/06']
}

activity_keywords = ['organização', 'teste', 'formação', 'treinamento', 'elaboração', 
                    'relatório', 'vistoria', 'suporte', 'reunião', 'desenvolvimento',
                    'atendimento', 'manutenção', 'análise', 'documentação', 'auditoria',
                    'levantamento', 'weekly', 'abertura', 'fechamento', 'controle']

activities_by_day = defaultdict(list)
current_day = None

for i, line in enumerate(lines):
    # Verificar se a linha é um cabeçalho de dia
    for day_name, patterns in day_patterns.items():
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                current_day = day_name
                print(f"\n>>> ENCONTRADO CABEÇALHO: {day_name} (linha {i}: {line})")
                break
    
    # Se estamos dentro de um dia, coletar atividades
    if current_day:
        line_lower = line.lower()
        # Verificar se é uma atividade
        if (any(kw in line_lower for kw in activity_keywords) and 
            10 < len(line) < 200 and
            not re.search(r'^\d{2}/\d{2}$', line) and
            not re.search(r'^\d{2}:\d{2}$', line) and
            not re.search(r'Horário|Matricula|Cargo|pág\.|Semana', line, re.IGNORECASE)):
            
            clean = re.sub(r'^\s*[•\-\*]\s*', '', line)
            clean = re.sub(r'\s+', ' ', clean).strip()
            
            if clean and clean not in activities_by_day[current_day]:
                activities_by_day[current_day].append(clean)
                print(f"  [{current_day}] {clean}")

print("\n" + "=" * 80)
print("RESUMO PÁGINA 2:")
print("=" * 80)
for day, acts in activities_by_day.items():
    print(f"{day}: {len(acts)} atividades")

print("\n" + "=" * 80)
print("PÁGINA 4 - LAISLA")
print("=" * 80)

page = doc[3]  # Página 4 (índice 3)
page_text = page.get_text()

lines = [l.strip() for l in page_text.split('\n') if l.strip()]

activities_by_day = defaultdict(list)
current_day = None

for i, line in enumerate(lines):
    # Verificar se a linha é um cabeçalho de dia
    for day_name, patterns in day_patterns.items():
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                current_day = day_name
                print(f"\n>>> ENCONTRADO CABEÇALHO: {day_name} (linha {i}: {line})")
                break
    
    # Se estamos dentro de um dia, coletar atividades
    if current_day:
        line_lower = line.lower()
        # Verificar se é uma atividade
        if (any(kw in line_lower for kw in activity_keywords) and 
            10 < len(line) < 200 and
            not re.search(r'^\d{2}/\d{2}$', line) and
            not re.search(r'^\d{2}:\d{2}$', line) and
            not re.search(r'Horário|Matricula|Cargo|pág\.|Semana', line, re.IGNORECASE)):
            
            clean = re.sub(r'^\s*[•\-\*]\s*', '', line)
            clean = re.sub(r'\s+', ' ', clean).strip()
            
            if clean and clean not in activities_by_day[current_day]:
                activities_by_day[current_day].append(clean)
                print(f"  [{current_day}] {clean}")

print("\n" + "=" * 80)
print("RESUMO PÁGINA 4:")
print("=" * 80)
for day, acts in activities_by_day.items():
    print(f"{day}: {len(acts)} atividades")

doc.close()
