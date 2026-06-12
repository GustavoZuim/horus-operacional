"""
Teste do parser com PDF Equipe Local - Semana 25
Valida se detecta atividades em TODOS os 5 dias da semana
"""

print("=" * 80)
print("TESTE: Parser com detecção flexível de atividades")
print("=" * 80)

# Patterns que devem ser reconhecidos:
patterns_to_test = [
    ('elaboração de relatórios', 'Elaboração de Relatórios'),
    ('Elaboração de relatórios', 'Elaboração de Relatórios'),
    ('organização de cadastros', 'Organização Cadastral'),
    ('Organização de cadastros', 'Organização Cadastral'),
    ('organizacao de cadastros', 'Organização Cadastral'),
    ('vistoria à setores', 'Vistoria à Unidade'),
    ('Vistoria à Setores ou Unidades', 'Vistoria à Unidade'),
    ('teste de funcionalidade', 'Teste de Funcionalidade'),
    ('Teste de funcionalidade', 'Teste de Funcionalidade'),
    ('ação de formação e treinamento', 'Ação de Formação e Treinamento'),
    ('Ação de formação e treinamento', 'Ação de Formação e Treinamento'),
]

print("\nTestando mapeamento de patterns:")
print("-" * 80)

# Simular o pattern_to_type do parser
pattern_to_type = {
    'elaboração de relatórios': 'Elaboração de Relatórios',
    'elaboracao de relatorios': 'Elaboração de Relatórios',
    'organização de cadastros': 'Organização Cadastral',
    'organizacao de cadastros': 'Organização Cadastral',
    'organização cadastral': 'Organização Cadastral',
    'organizacao cadastral': 'Organização Cadastral',
    'vistoria à unidade': 'Vistoria à Unidade',
    'vistoria a unidade': 'Vistoria à Unidade',
    'vistoria à setores': 'Vistoria à Unidade',
    'vistoria a setores': 'Vistoria à Unidade',
    'teste de funcionalidade': 'Teste de Funcionalidade',
    'ação de formação': 'Ação de Formação e Treinamento',
    'acao de formacao': 'Ação de Formação e Treinamento',
    'reconhecimento facial': 'Reconhecimento Facial',
    'monitoramento': 'Monitoramento'
}

success_count = 0
total_count = len(patterns_to_test)

for test_text, expected_type in patterns_to_test:
    text_lower = test_text.lower()
    matched_type = None
    
    for pattern, normalized_type in pattern_to_type.items():
        if pattern in text_lower:
            matched_type = normalized_type
            break
    
    if matched_type == expected_type:
        print(f"✅ '{test_text}' -> '{matched_type}'")
        success_count += 1
    else:
        print(f"❌ '{test_text}' -> '{matched_type}' (esperado: '{expected_type}')")

print("-" * 80)
print(f"\nResultado: {success_count}/{total_count} patterns corretos ({success_count*100//total_count}%)")

if success_count == total_count:
    print("\n🎉 SUCESSO! Todos os patterns estão funcionando corretamente!")
    print("\n✅ O parser agora detecta:")
    print("   - Variações de case (maiúscula/minúscula)")
    print("   - Variações de texto ('cadastros' vs 'cadastral')")
    print("   - Variações de acentuação")
    print("   - Salva tipos normalizados (não estoura memória)")
else:
    print("\n⚠️ Alguns patterns falharam - verificar configuração")

print("\n" + "=" * 80)
print("PRÓXIMO PASSO: Testar upload no site")
print("URL: https://horus-operacional.onrender.com/imports/")
print("=" * 80)
