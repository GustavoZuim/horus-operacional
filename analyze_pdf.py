# -*- coding: utf-8 -*-
"""
Teste SIMPLES do parser com PDF real - SEM Flask
"""
import fitz
import re

pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"

print("=" * 80)
print("ANÁLISE DO PDF REAL")
print("=" * 80)

# Abrir PDF
doc = fitz.open(pdf_path)
print(f"\n📄 PDF: {pdf_path}")
print(f"📊 Total de páginas: {len(doc)}")

# Extrair texto de cada página
print("\n" + "=" * 80)
print("ANÁLISE PÁGINA POR PÁGINA:")
print("=" * 80)

for page_num in range(len(doc)):
    page = doc[page_num]
    page_text = page.get_text()
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    
    print(f"\n📄 PÁGINA {page_num + 1}:")
    print("-" * 80)
    
    # Mostrar primeiras 20 linhas
    print("Primeiras 20 linhas:")
    for i, line in enumerate(lines[:20], 1):
        print(f"  {i:2d}: {line}")
    
    # Buscar matrículas
    print("\n🔍 Buscando matrículas:")
    mat_patterns = [
        (r'Matr[íi]cula\s*[:\-]?\s*([A-Z]{1,3}\d+)', 'Padrão AB123/ABC1234'),
        (r'Matr[íi]cula\s*[:\-]?\s*([a-z]+\.[a-z]+)', 'Padrão email (h.carmo)'),
        (r'Matr[íi]cula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)', 'Padrão Mediador MF36'),
        (r'Matr[íi]cula\s*[:\-]?\s*([A-Z]\d+)', 'Padrão simples P01'),
        (r'Matricula\s*[:\-]?\s*([A-Z]{1,3}\d+)', 'Matricula sem acento'),
        (r'Matricula\s*[:\-]?\s*([a-z]+\.[a-z]+)', 'Matricula email'),
        (r'Matricula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)', 'Matricula Mediador'),
        (r'Matricula\s*[:\-]?\s*([A-Z]\d+)', 'Matricula simples'),
    ]
    
    found_any = False
    for pattern, desc in mat_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        if matches:
            found_any = True
            for match in matches:
                print(f"  ✅ {desc}: {match}")
                # Buscar nome próximo
                for j, line in enumerate(lines):
                    if match in line or 'Matr' in line:
                        # Pegar linhas ao redor
                        print(f"     Contexto (linhas {max(0, j-3)} a {min(len(lines), j+3)}):")
                        for k in range(max(0, j-3), min(len(lines), j+3)):
                            marker = " >>> " if k == j else "     "
                            print(f"{marker}{lines[k]}")
                        break
                print()
    
    if not found_any:
        print("  ❌ Nenhuma matrícula detectada")
    
    print()

doc.close()

print("=" * 80)
print("FIM DA ANÁLISE")
print("=" * 80)
