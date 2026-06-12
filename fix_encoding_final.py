# -*- coding: utf-8 -*-
"""
Script DEFINITIVO para corrigir encoding em TODOS os arquivos
Corrige TODOS os caracteres ✅? possíveis
"""
import os
import re

# Dicionário COMPLETO de substituições
REPLACEMENTS = {
    # Vogais com acento agudo
    'Ü': 'á',
    'Ü': 'é',
    'Ü': 'í',
    'Ü': 'ó',
    'Ü': 'ú',
    'Ü': 'Á',
    'Ü': 'É',
    'Ü': 'Í',
    'Ü': 'Ó',
    'Ü': 'Ú',
    
    # Vogais com acento circunflexo
    'Ü': 'â',
    'Ü': 'ê',
    'Ü': 'ô',
    'Ü': 'Â',
    'Ü': 'Ê',
    'Ü': 'Ô',
    
    # Vogais com til
    'Ü': 'ã',
    'Ü': 'õ',
    'Ü': 'Ã',
    'Ü': 'Õ',
    
    # Cedilha
    'Ü': 'ç',
    'Ü': 'Ç',
    
    # Vogais com trema
    'Ü': 'ü',
    'Ü': 'Ü',
    
    # Combinações específicas encontradas
    'Hórus': 'Hórus',
    'hórus': 'hórus',
    'Operação': 'Operação',
    'operação': 'operação',
    'Validação': 'Validação',
    'validação': 'validação',
    'Período': 'Período',
    'período': 'período',
    'Atenção': 'Atenção',
    'atenção': 'atenção',
    'Administração': 'Administração',
    'administração': 'administração',
    'Observação': 'Observação',
    'observação': 'observação',
    'ação': 'ação',
    'ações': 'ações',
    'Ações': 'Ações',
    'Ação': 'Ação',
    'não': 'não',
    'estão': 'estão',
    'serão': 'serão',
    'Configuração': 'Configuração',
    'configuração': 'configuração',
    'Tradução': 'Tradução',
    'tradução': 'tradução',
    'aplicação': 'aplicação',
    'Aplicação': 'Aplicação',
    'usuário': 'usuário',
    'Usuário': 'Usuário',
    'autenticação': 'autenticação',
    'Autenticação': 'Autenticação',
    'Utilitários': 'Utilitários',
    'utilitários': 'utilitários',
    'inicialização': 'inicialização',
    'Inicialização': 'Inicialização',
    'Distribuição': 'Distribuição',
    'distribuição': 'distribuição',
    'Lágrima': 'Lágrima',
    'mística': 'mística',
    'símbolo': 'símbolo',
    'proteção': 'proteção',
    'opção': 'opção',
    'Opção': 'Opção',
    'Criação': 'Criação',
    'criação': 'criação',
    'rápida': 'rápida',
    'Rápida': 'Rápida',
    'Atualização': 'Atualização',
    'atualização': 'atualização',
    'Exportação': 'Exportação',
    'exportação': 'exportação',
    'Últimas': 'Últimas',
    'Inicialização': 'Inicialização',
    'seções': 'seções',
    'Seções': 'Seções',
    'Gestão': 'Gestão',
    'gestão': 'gestão',
    'exceção': 'exceção',
    'Exceção': 'Exceção',
    'exibição': 'exibição',
    'Exibição': 'Exibição',
    'alteração': 'alteração',
    'Alteração': 'Alteração',
    'alterações': 'alterações',
    'Alterações': 'Alterações',
    'informação': 'informação',
    'Informação': 'Informação',
    'Navegação': 'Navegação',
    'navegação': 'navegação',
    'classificações': 'classificações',
    'Classificações': 'Classificações',
    'Terça': 'Terça',
    'terça': 'terça',
    'compensatória': 'compensatória',
    'Compensatória': 'Compensatória',
    'EXTRAÇÃO': 'EXTRAÇÃO',
    'PÁGINA': 'PÁGINA',
    'Matrícula': 'Matrícula',
    'matrícula': 'matrícula',
    'integração': 'integração',
    'Integração': 'Integração',
    'Capacitação': 'Capacitação',
    'capacitação': 'capacitação',
    'produção': 'produção',
    'Produção': 'Produção',
    'descrições': 'descrições',
    'Descrições': 'Descrições',
    'confirmação': 'confirmação',
    'Confirmação': 'Confirmação',
    'Função': 'Função',
    'função': 'função',
    'ATENÇÃO': 'ATENÇÃO',
    'revisível': 'revisível',
    'Revisível': 'Revisível',
    'prévia': 'prévia',
    'Prévia': 'Prévia',
    'Gestão por exceção': 'Gestão por exceção',
    'vê': 'vê',
    'Formulário': 'Formulário',
    'formulário': 'formulário',
    
    # Emojis e símbolos especiais (corrigir)
    '🗑️': '🗑️',
    '✅': '✅',
    '✓': '✅',
    '✓': '✓',
        # Casos específicos de ç antes de a, o, u
    'começam': 'começam',
    'começar': 'começar',
    'começa': 'começa',
    'faça': 'faça',
    'cabeça': 'cabeça',
    'espaço': 'espaço',
    'avançar': 'avançar',
    'lançar': 'lançar',
    'alcançar': 'alcançar',
    'dança': 'dança',
    'preço': 'preço',
    'força': 'força',
        # Padrões regex para capturar qualquer ✓ restante
}

def fix_file(filepath):
    """Corrige encoding em um arquivo"""
    try:
        # Ler arquivo
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Aplicar todas as substituições
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Se houve mudanças, salvar
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f'Erro em {filepath}: {e}')
        return False

def main():
    """Processa todos os arquivos"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Extensões a processar
    extensions = ['.py', '.html', '.js', '.css', '.md', '.txt', '.json']
    
    fixed_count = 0
    total_count = 0
    
    # Procurar e corrigir arquivos
    for root, dirs, files in os.walk(base_dir):
        # Pular diretórios irrelevantes
        if any(skip in root for skip in ['venv', '__pycache__', '.git', 'node_modules']):
            continue
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                total_count += 1
                
                if fix_file(filepath):
                    fixed_count += 1
                    print(f'✅ Corrigido: {os.path.relpath(filepath, base_dir)}')
    
    print(f'\n✅ CONCLUÍDO!')
    print(f'   Arquivos verificados: {total_count}')
    print(f'   Arquivos corrigidos: {fixed_count}')

if __name__ == '__main__':
    main()
