# -*- coding: utf-8 -*-
"""
Teste DIRETO dos padrões de regex
"""
import re

# Textos reais do PDF
test_cases = [
    ("Guilherme Stawichs\nMatricula: P01 Cargo: - Autor: Nathani Borges", "P01"),
    ("Hortencia Carmo\nMatricula: h.carmo Cargo: Administrador do Sistema", "h.carmo"),
    ("Laisla Moraes dos Santos\nMatricula: Mediador MF36 Cargo: Assistente Administrativo", "Mediador MF36"),
]

patterns = [
    (r'Matr[íi]cula\s*[:\-]?\s*([A-Z]{1,3}\d+)', 'Padrão AB123/ABC1234'),
    (r'Matr[íi]cula\s*[:\-]?\s*([a-z]+\.[a-z]+)', 'Padrão email (h.carmo)'),
    (r'Matr[íi]cula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)', 'Padrão Mediador MF36'),
    (r'Matr[íi]cula\s*[:\-]?\s*([A-Z]\d+)', 'Padrão simples P01'),
    (r'Matricula\s*[:\-]?\s*([A-Z]{1,3}\d+)', 'Matricula sem acento'),
    (r'Matricula\s*[:\-]?\s*([a-z]+\.[a-z]+)', 'Matricula email'),
    (r'Matricula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)', 'Matricula Mediador'),
    (r'Matricula\s*[:\-]?\s*([A-Z]\d+)', 'Matricula simples'),
]

print("=" * 80)
print("TESTE DE REGEX PATTERNS")
print("=" * 80)

for text, expected in test_cases:
    print(f"\n📄 Texto: {text[:50]}...")
    print(f"✅ Esperado: {expected}")
    print("-" * 80)
    
    found = False
    for pattern, desc in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found = True
            print(f"  ✅ {desc}: {matches}")
    
    if not found:
        print(f"  ❌ NENHUM PADRÃO DETECTOU!")

print("\n" + "=" * 80)
