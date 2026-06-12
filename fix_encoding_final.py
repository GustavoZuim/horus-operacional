# -*- coding: utf-8 -*-
"""
Script DEFINITIVO para corrigir encoding em TODOS os arquivos
Corrige TODOS os caracteres ÜÜ? possíveis
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
    'HÜrus': 'Hórus',
    'hÜrus': 'hórus',
    'OperaÜÜo': 'Operação',
    'operaÜÜo': 'operação',
    'ValidaÜÜo': 'Validação',
    'validaÜÜo': 'validação',
    'PerÜodo': 'Período',
    'perÜodo': 'período',
    'AtenÜÜo': 'Atenção',
    'atenÜÜo': 'atenção',
    'AdministraÜÜo': 'Administração',
    'administraÜÜo': 'administração',
    'ObservaÜÜo': 'Observação',
    'observaÜÜo': 'observação',
    'aÜÜo': 'ação',
    'aÜÜes': 'ações',
    'AÜÜes': 'Ações',
    'AÜÜo': 'Ação',
    'nÜo': 'não',
    'estÜo': 'estão',
    'serÜo': 'serão',
    'ConfiguraÜÜo': 'Configuração',
    'configuraÜÜo': 'configuração',
    'TraduÜÜo': 'Tradução',
    'traduÜÜo': 'tradução',
    'aplicaÜÜo': 'aplicação',
    'AplicaÜÜo': 'Aplicação',
    'usuÜrio': 'usuário',
    'UsuÜrio': 'Usuário',
    'autenticaÜÜo': 'autenticação',
    'AutenticaÜÜo': 'Autenticação',
    'UtilitÜrios': 'Utilitários',
    'utilitÜrios': 'utilitários',
    'inicializaÜÜo': 'inicialização',
    'InicializaÜÜo': 'Inicialização',
    'DistribuiÜÜo': 'Distribuição',
    'distribuiÜÜo': 'distribuição',
    'LÜgrima': 'Lágrima',
    'mÜtica': 'mística',
    'sÜmbolo': 'símbolo',
    'proteÜÜo': 'proteção',
    'opÜÜo': 'opção',
    'OpÜÜo': 'Opção',
    'CriaÜÜo': 'Criação',
    'criaÜÜo': 'criação',
    'rÜpida': 'rápida',
    'RÜpida': 'Rápida',
    'AtualizaÜÜo': 'Atualização',
    'atualizaÜÜo': 'atualização',
    'ExportaÜÜo': 'Exportação',
    'exportaÜÜo': 'exportação',
    'Ültimas': 'Últimas',
    'InicializaÜÜo': 'Inicialização',
    'seÜÜes': 'seções',
    'SeÜÜes': 'Seções',
    'GestÜo': 'Gestão',
    'gestÜo': 'gestão',
    'exceÜÜo': 'exceção',
    'ExceÜÜo': 'Exceção',
    'exibiÜÜo': 'exibição',
    'ExibiÜÜo': 'Exibição',
    'alteraÜÜo': 'alteração',
    'AlteraÜÜo': 'Alteração',
    'alteraÜÜes': 'alterações',
    'AlteraÜÜes': 'Alterações',
    'informaÜÜo': 'informação',
    'InformaÜÜo': 'Informação',
    'NavegaÜÜo': 'Navegação',
    'navegaÜÜo': 'navegação',
    'classificaÜÜes': 'classificações',
    'ClassificaÜÜes': 'Classificações',
    'TerÜa': 'Terça',
    'terÜa': 'terça',
    'compensatÜria': 'compensatória',
    'CompensatÜria': 'Compensatória',
    'EXTRAÜÜO': 'EXTRAÇÃO',
    'PÜGINA': 'PÁGINA',
    'MatrÜcula': 'Matrícula',
    'matrÜcula': 'matrícula',
    'integraÜÜo': 'integração',
    'IntegraÜÜo': 'Integração',
    'CapacitaÜÜo': 'Capacitação',
    'capacitaÜÜo': 'capacitação',
    'produÜÜo': 'produção',
    'ProduÜÜo': 'Produção',
    'descriÜÜes': 'descrições',
    'DescriÜÜes': 'Descrições',
    'confirmaÜÜo': 'confirmação',
    'ConfirmaÜÜo': 'Confirmação',
    'FunÜÜo': 'Função',
    'funÜÜo': 'função',
    'ATENÜÜO': 'ATENÇÃO',
    'revisÜvel': 'revisível',
    'RevisÜvel': 'Revisível',
    'prÜvia': 'prévia',
    'PrÜvia': 'Prévia',
    'GestÜo por exceÜÜo': 'Gestão por exceção',
    'vÜ': 'vê',
    'FormulÜrio': 'Formulário',
    'formulÜrio': 'formulário',
    
    # Emojis e símbolos especiais (corrigir)
    'ÜÜÜ?': '🗑️',
    'ÜÜ': '✅',
    'Ü?': '✅',
    'Ü?': '✓',
    
    # Padrões regex para capturar qualquer Ü? restante
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
