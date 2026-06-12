"""Ver todos os textos da página 5"""
import fitz

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

page = doc[4]  # Página 5
text = page.get_text()

print("=" * 100)
print("PÁGINA 5 - TEXTO COMPLETO")
print("=" * 100)
print(text)

doc.close()
