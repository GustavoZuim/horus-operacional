"""Analisar posições página 5"""
import fitz

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

page = doc[4]  # Página 5
blocks = page.get_text("dict")["blocks"]

print("=" * 100)
print("PÁGINA 5 - POSIÇÕES DOS CARDS")
print("=" * 100)

activity_types = [
    'Elaboração de Relatórios',
    'Organização Cadastral',
    'Vistoria à Unidade',
    'Teste de Funcionalidade',
    'Ação de Formação e Treinamento'
]

for block in blocks:
    if block['type'] == 0:
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                y = span['bbox'][1]
                
                for act_type in activity_types:
                    if act_type in text:
                        print(f"X={x:6.1f}, Y={y:6.1f}: {text}")

doc.close()
