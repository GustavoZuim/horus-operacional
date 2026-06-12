"""Teste isolado do parser"""
import fitz
from collections import defaultdict

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"

def extract_activities_by_day_v3(pdf_path, page_num):
    """Extrai atividades usando coordenadas X/Y - conta CARDS, não linhas
    
    ESTRATÉGIA FINAL:
    - Detecta posições X dos cabeçalhos dos dias
    - Detecta cards pelos cabeçalhos de tipo
    - Para cada card, determina qual cabeçalho de dia está mais próximo
    """
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
    
    # 1. Detectar posições X dos cabeçalhos dos dias
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
    
    # 2. Tipos de cards
    activity_types = [
        'Elaboração de Relatórios',
        'Organização Cadastral',
        'Vistoria à Unidade',
        'Teste de Funcionalidade',
        'Ação de Formação e Treinamento'
    ]
    
    # 3. Detectar TODOS os cards e mapear para dia mais próximo
    y_threshold = 100
    detected_cards = {}  # Para evitar duplicatas exatas
    
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
                                    # Chave única para evitar duplicatas exatas
                                    card_key = f"{closest_day}_{act_type}_{int(y)}"
                                    if card_key not in detected_cards:
                                        activities_by_day[closest_day].append(act_type)
                                        detected_cards[card_key] = True
    
    doc.close()
    return activities_by_day

print("=" * 100)
print("TESTE DO NOVO PARSER V3 - CONTAGEM POR COORDENADAS")
print("=" * 100)

# Testar página 2 (Hortencia)
print("\nPÁGINA 2 - HORTENCIA:")
page2_activities = extract_activities_by_day_v3(pdf_path, 1)
for day, acts in page2_activities.items():
    day_names = {'monday': 'Segunda', 'tuesday': 'Terça', 'wednesday': 'Quarta', 
                  'thursday': 'Quinta', 'friday': 'Sexta'}
    print(f"{day_names[day]}: {len(acts)} atividades")
    if acts:
        for i, act in enumerate(acts, 1):
            print(f"  {i}. {act}")

# Testar página 4 (Laisla)
print("\n" + "=" * 100)
print("PÁGINA 4 - LAISLA:")
page4_activities = extract_activities_by_day_v3(pdf_path, 3)
for day, acts in page4_activities.items():
    day_names = {'monday': 'Segunda', 'tuesday': 'Terça', 'wednesday': 'Quarta', 
                  'thursday': 'Quinta', 'friday': 'Sexta'}
    print(f"{day_names[day]}: {len(acts)} atividades")
    if acts:
        for i, act in enumerate(acts, 1):
            print(f"  {i}. {act}")

print("\n" + "=" * 100)
print("RESULTADO ESPERADO:")
print("=" * 100)
print("Hortencia Segunda: 7 atividades")
print("Laisla Segunda: 6 atividades")
