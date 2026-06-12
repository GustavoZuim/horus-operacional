# -*- coding: utf-8 -*-
"""
Teste com estrutura EXATA do PDF
"""
import re

# Estrutura real da página 1 do PDF
page_1_lines = [
    "Planejamento Semanal - Equipe Local",
    "Semana 25",
    "10/06/2026 16:20 pág. 1/6",
    "Guilherme Stawichs",
    "Matricula: P01 Cargo: - Autor: Nathani Borges",
    "Horário de Início: 08:00 Horário de Finalização: 17:00",
    "Segunda-feira",
    "15/06"
]

# Estrutura da página 2 do PDF
page_2_lines = [
    "Planejamento Semanal - Equipe Local",
    "Semana 25",
    "10/06/2026 16:20 pág. 2/6",
    "Hortencia Carmo",
    "Matricula: h.carmo Cargo: Administrador do Sistema Autor: Nathani Borges",
    "Horário de Início: 08:00 Horário de Finalização: 17:00",
    "Segunda-feira",
    "15/06"
]

# Estrutura da página 4 do PDF
page_4_lines = [
    "Planejamento Semanal - Equipe Local",
    "Semana 25",
    "10/06/2026 16:20 pág. 4/6",
    "Laisla Moraes dos Santos",
    "Matricula: Mediador MF36 Cargo: Assistente Administrativo Autor: Nathani Borges",
    "Horário de Início: 08:00 Horário de Finalização: 17:00",
    "Segunda-feira",
    "15/06"
]

def extract_professionals_from_lines(lines):
    """Simula a lógica do parser"""
    professionals = []
    
    mat_patterns = [
        r'Matr[íi]cula\s*[:\-]?\s*([A-Z]{1,3}\d+)',
        r'Matricula\s*[:\-]?\s*([A-Z]{1,3}\d+)',
        r'Matr[íi]cula\s*[:\-]?\s*([a-z]+\.[a-z]+)',
        r'Matricula\s*[:\-]?\s*([a-z]+\.[a-z]+)',
        r'Matr[íi]cula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)',
        r'Matricula\s*[:\-]?\s*(Mediador\s+[A-Z0-9]+)',
        r'Matr[íi]cula\s*[:\-]?\s*([A-Z]\d+)',
        r'Matricula\s*[:\-]?\s*([A-Z]\d+)',
    ]
    
    for i, line in enumerate(lines):
        for pattern in mat_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                matricula = match.group(1).upper()
                print(f"  🔍 Linha {i}: Encontrou matrícula '{matricula}' em: {line}")
                
                # Buscar nome nas linhas anteriores
                nome = None
                for j in range(max(0, i-5), i):
                    candidate = lines[j]
                    print(f"     Checando linha {j} (antes): {candidate}")
                    if (len(candidate) > 5 and 
                        candidate[0].isupper() and 
                        len(candidate.split()) >= 2 and
                        not re.search(r'Matr[íi]cula|Cargo|Função|Semana', candidate, re.IGNORECASE)):
                        nome = candidate
                        print(f"     ✅ Nome encontrado: {nome}")
                        break
                
                if not nome:
                    print(f"     ⚠️  Nome não encontrado antes, buscando depois...")
                    for j in range(i+1, min(len(lines), i+3)):
                        candidate = lines[j]
                        print(f"     Checando linha {j} (depois): {candidate}")
                        if (len(candidate) > 5 and 
                            candidate[0].isupper() and 
                            len(candidate.split()) >= 2 and
                            not re.search(r'Matr[íi]cula|Cargo|Função', candidate, re.IGNORECASE)):
                            nome = candidate
                            print(f"     ✅ Nome encontrado: {nome}")
                            break
                
                if nome:
                    professionals.append({'name': nome, 'registration': matricula})
                    print(f"  ✅ Profissional adicionado: {nome} ({matricula})\n")
                else:
                    print(f"  ❌ NOME NÃO ENCONTRADO para matrícula {matricula}!\n")
                break
    
    return professionals

print("=" * 80)
print("TESTE COM ESTRUTURA EXATA DO PDF")
print("=" * 80)

print("\n📄 PÁGINA 1 (Guilherme Stawichs - P01):")
print("-" * 80)
profs_1 = extract_professionals_from_lines(page_1_lines)
print(f"Resultado: {profs_1}")

print("\n📄 PÁGINA 2 (Hortencia Carmo - h.carmo):")
print("-" * 80)
profs_2 = extract_professionals_from_lines(page_2_lines)
print(f"Resultado: {profs_2}")

print("\n📄 PÁGINA 4 (Laisla Moraes dos Santos - Mediador MF36):")
print("-" * 80)
profs_4 = extract_professionals_from_lines(page_4_lines)
print(f"Resultado: {profs_4}")

print("\n" + "=" * 80)
print(f"TOTAL: {len(profs_1) + len(profs_2) + len(profs_4)} profissionais detectados")
print("=" * 80)
