"""Teste do novo parser com coordenadas"""
import sys
sys.path.append('c:\\Users\\Gustavo\\Desktop\\horus-operacional')

from app.ai_parser import PlanningAIParser

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"

parser = PlanningAIParser(pdf_path)

print("=" * 100)
print("TESTE DO NOVO PARSER V3 - CONTAGEM POR COORDENADAS")
print("=" * 100)

# Testar página 2 (Hortencia)
print("\nPÁGINA 2 - HORTENCIA:")
page2_activities = parser.extract_activities_by_day_v3(1)  # Índice 1 = página 2
for day, acts in page2_activities.items():
    day_names = {'monday': 'Segunda', 'tuesday': 'Terça', 'wednesday': 'Quarta', 
                  'thursday': 'Quinta', 'friday': 'Sexta'}
    print(f"{day_names[day]}: {len(acts)} atividades")
    for i, act in enumerate(acts, 1):
        print(f"  {i}. {act}")

# Testar página 4 (Laisla)
print("\n" + "=" * 100)
print("PÁGINA 4 - LAISLA:")
page4_activities = parser.extract_activities_by_day_v3(3)  # Índice 3 = página 4
for day, acts in page4_activities.items():
    day_names = {'monday': 'Segunda', 'tuesday': 'Terça', 'wednesday': 'Quarta', 
                  'thursday': 'Quinta', 'friday': 'Sexta'}
    print(f"{day_names[day]}: {len(acts)} atividades")
    for i, act in enumerate(acts, 1):
        print(f"  {i}. {act}")

print("\n" + "=" * 100)
print("RESULTADO ESPERADO:")
print("=" * 100)
print("Hortencia Segunda: 7 atividades")
print("Laisla Segunda: 6 atividades")
