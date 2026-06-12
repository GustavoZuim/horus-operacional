"""Ver todas as posições X"""
import fitz

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"
doc = fitz.open(pdf_path)

page = doc[1]
blocks = page.get_text("dict")["blocks"]

print("=" * 80)
print("TODAS AS POSIÇÕES X (primeiros 50 textos)")
print("=" * 80)

count = 0
for block in blocks:
    if block['type'] == 0 and count < 50:  # Texto
        for line in block['lines']:
            for span in line['spans']:
                text = span['text'].strip()
                x = span['bbox'][0]
                if text and count < 50:
                    print(f"X={x:6.1f}: {text[:70]}")
                    count += 1

doc.close()
