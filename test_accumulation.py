"""Teste de acumulação multi-página"""
import fitz
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"

def extract_activities_by_day_v3(pdf_path, page_num):
    """Extrai atividades de UMA página"""
    activities_by_day = {
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': []
    }
    
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):
        doc.close()
        return activities_by_day
    
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    
    # Detectar posições X dos cabeçalhos dos dias
    day_headers = {}
    for block in blocks:
        if block['type'] == 0:
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    x = span['bbox'][0]
                    
                    if 'Segunda-feira' in text:
                        day_headers['monday'] = x
                    elif 'Terça-feira' in text or 'Terca-feira' in text:
                        day_headers['tuesday'] = x
                    elif 'Quarta-feira' in text:
                        day_headers['wednesday'] = x
                    elif 'Quinta-feira' in text:
                        day_headers['thursday'] = x
                    elif 'Sexta-feira' in text:
                        day_headers['friday'] = x
    
    if not day_headers:
        doc.close()
        return activities_by_day
    
    # Tipos de cards
    activity_types = [
        'Elaboração de Relatórios',
        'Organização Cadastral',
        'Vistoria à Unidade',
        'Teste de Funcionalidade',
        'Ação de Formação e Treinamento'
    ]
    
    # Detectar cards e mapear para dia mais próximo
    y_threshold = 80  # Threshold mais baixo
    detected_cards = {}
    
    for block in blocks:
        if block['type'] == 0:
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    x = span['bbox'][0]
                    y = span['bbox'][1]
                    
                    if y > y_threshold:
                        for act_type in activity_types:
                            if act_type in text:
                                # Determinar qual cabeçalho de dia está mais próximo
                                closest_day = None
                                min_distance = float('inf')
                                
                                for day, header_x in day_headers.items():
                                    distance = abs(x - header_x)
                                    if distance < min_distance:
                                        min_distance = distance
                                        closest_day = day
                                
                                if closest_day:
                                    card_key = f"{closest_day}_{act_type}_{int(y)}"
                                    if card_key not in detected_cards:
                                        activities_by_day[closest_day].append(act_type)
                                        detected_cards[card_key] = True
    
    doc.close()
    return activities_by_day

print("=" * 100)
print("TESTE DE ACUMULAÇÃO MULTI-PÁGINA")
print("=" * 100)

# Hortencia: página 2 + página 3
print("\nHORTENCIA:")
print("-" * 100)
page2_acts = extract_activities_by_day_v3(pdf_path, 1)  # Página 2
page3_acts = extract_activities_by_day_v3(pdf_path, 2)  # Página 3

# Acumular
hortencia_total = defaultdict(list)
for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
    hortencia_total[day] = page2_acts[day] + page3_acts[day]

day_names = {'monday': 'Segunda', 'tuesday': 'Terça', 'wednesday': 'Quarta', 
              'thursday': 'Quinta', 'friday': 'Sexta'}

print("\nPágina 2:")
for day, acts in page2_acts.items():
    print(f"  {day_names[day]}: {len(acts)} atividades")

print("\nPágina 3:")
for day, acts in page3_acts.items():
    print(f"  {day_names[day]}: {len(acts)} atividades")

print("\nTOTAL HORTENCIA:")
for day, acts in hortencia_total.items():
    expected = {'monday': 7, 'tuesday': 5, 'wednesday': 7, 'thursday': 7, 'friday': 6}
    result = "✅" if len(acts) == expected[day] else f"❌ (esperado: {expected[day]})"
    print(f"  {day_names[day]}: {len(acts)} atividades {result}")

# Laisla: página 4 + página 5
print("\n" + "=" * 100)
print("LAISLA:")
print("-" * 100)
page4_acts = extract_activities_by_day_v3(pdf_path, 3)  # Página 4
page5_acts = extract_activities_by_day_v3(pdf_path, 4)  # Página 5

# Acumular
laisla_total = defaultdict(list)
for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
    laisla_total[day] = page4_acts[day] + page5_acts[day]

print("\nPágina 4:")
for day, acts in page4_acts.items():
    print(f"  {day_names[day]}: {len(acts)} atividades")

print("\nPágina 5:")
for day, acts in page5_acts.items():
    print(f"  {day_names[day]}: {len(acts)} atividades")

print("\nTOTAL LAISLA:")
for day, acts in laisla_total.items():
    expected = {'monday': 6, 'tuesday': 3, 'wednesday': 3, 'thursday': 3, 'friday': 4}
    result = "✅" if len(acts) == expected[day] else f"❌ (esperado: {expected[day]})"
    print(f"  {day_names[day]}: {len(acts)} atividades {result}")
