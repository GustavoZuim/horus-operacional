"""Ver texto bruto do PDF"""
import fitz

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

# Página 2 - Hortencia
print("=" * 80)
print("PÁGINA 2 - TEXTO BRUTO (primeiras 100 linhas)")
print("=" * 80)
page = doc[1]
text = page.get_text()
lines = text.split('\n')
for i, line in enumerate(lines[:100]):
    if line.strip():
        print(f"{i:3d}: {line}")

doc.close()
