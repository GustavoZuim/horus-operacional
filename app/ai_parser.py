"""
Agente de IA para interpreta????o inteligente de PDFs de planejamento
Usa t??cnicas avan??adas de NLP e extra????o estruturada
"""
import fitz  # PyMuPDF
import re
from typing import Dict, List, Tuple
from datetime import datetime

class PlanningAIParser:
    """Parser inteligente com t??cnicas de IA para extrair dados estruturados de PDFs"""
    
    # Dias da semana em portugu??s
    WEEKDAYS = {
        'segunda': 'monday',
        'ter??a': 'tuesday',
        'quarta': 'wednesday',
        'quinta': 'thursday',
        'sexta': 'friday'
    }
    
    # Categorias de atividades comuns
    ACTIVITY_CATEGORIES = [
        'Organiza????o Cadastral',
        'Teste de Funcionalidades',
        'Forma????o e Treinamento',
        'Elabora????o de Relat??rios',
        'Vistoria ?? Setores ou Unidades',
        'Suporte T??cnico',
        'Reuni??o',
        'Desenvolvimento'
    ]
    
    def __init__(self, pdf_path: str):
        """Inicializa o parser com o caminho do PDF"""
        self.pdf_path = pdf_path
        self.text = self.extract_text()
        self.pages_text = self.extract_pages_text()
    
    def extract_text(self) -> str:
        """Extrai todo o texto do PDF"""
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_pages_text(self) -> List[str]:
        """Extrai texto de cada p??gina separadamente"""
        doc = fitz.open(self.pdf_path)
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        return pages
    
    def extract_week_info(self) -> Dict:
        """Extrai informa????es da semana"""
        result = {
            'week_label': None,
            'dates': []
        }
        
        # Buscar "Semana XX"
        week_match = re.search(r'Semana\s+(\d+)', self.text, re.IGNORECASE)
        if week_match:
            result['week_label'] = f"Semana {week_match.group(1)}"
        
        # Buscar todas as datas (dd/mm/yyyy ou dd/mm/yy)
        date_pattern = r'\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b'
        dates = re.findall(date_pattern, self.text)
        
        parsed_dates = []
        for day, month, year in dates:
            try:
                if len(year) == 2:
                    year = '20' + year
                date_obj = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
                if date_obj not in parsed_dates:
                    parsed_dates.append(date_obj)
            except:
                pass
        
        if parsed_dates:
            parsed_dates.sort()
            result['dates'] = parsed_dates
        
        return result
    
    def extract_project_name(self) -> str:
        """
        Extrai o nome do projeto do PDF usando IA
        
        Estratégia:
        1. Buscar padrão "Projeto: Nome"
        2. Buscar "Projeto Nome" no início do documento
        3. Buscar títulos em destaque no cabeçalho
        4. Extrair do nome do arquivo
        5. Fallback: "Projeto Sem Nome"
        """
        # Usar apenas as primeiras 3 páginas (onde geralmente está o projeto)
        first_pages = '\n'.join(self.pages_text[:min(3, len(self.pages_text))])
        
        # Padrão 1: "Projeto: Nome do Projeto"
        pattern1 = r'Projeto\s*:\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][^\n]{3,80})'
        match1 = re.search(pattern1, first_pages, re.IGNORECASE)
        if match1:
            project_name = match1.group(1).strip()
            # Limpar caracteres especiais do final
            project_name = re.sub(r'[\s\-_:]+$', '', project_name)
            return project_name
        
        # Padrão 2: "PROJETO Nome" ou "Project Nome"
        pattern2 = r'(?:PROJETO|Project)\s+([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][^\n]{3,80})'
        match2 = re.search(pattern2, first_pages)
        if match2:
            project_name = match2.group(1).strip()
            project_name = re.sub(r'[\s\-_:]+$', '', project_name)
            return project_name
        
        # Padrão 3: Buscar linha com palavras-chave e capitalização
        # Ex: "Educação Digital" ou "Sistema de Gestão"
        pattern3 = r'^([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+(?:\s+(?:de|da|do|dos|das|e|para|com))?\s+[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+(?:\s+[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+)*)'
        lines = first_pages.split('\n')
        for line in lines[:50]:  # Primeiras 50 linhas
            line = line.strip()
            if len(line) > 10 and len(line) < 80:
                match3 = re.match(pattern3, line)
                if match3:
                    potential_name = match3.group(1).strip()
                    # Verificar se não é uma categoria comum
                    common_words = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'matrícula', 'cargo', 'semana']
                    if not any(word in potential_name.lower() for word in common_words):
                        return potential_name
        
        # Padrão 4: Buscar no nome do arquivo
        # Ex: "planejamento_projeto_educacao.pdf"
        import os
        filename = os.path.basename(self.pdf_path)
        filename_no_ext = os.path.splitext(filename)[0]
        
        # Remover timestamps
        filename_clean = re.sub(r'\d{8}_\d{6}_', '', filename_no_ext)
        filename_clean = re.sub(r'planejamento[_\s]', '', filename_clean, flags=re.IGNORECASE)
        filename_clean = re.sub(r'[_-]', ' ', filename_clean)
        
        if len(filename_clean) > 5 and len(filename_clean) < 80:
            # Capitalizar
            words = filename_clean.split()
            capitalized = ' '.join(word.capitalize() for word in words)
            if capitalized != 'Semana' and not capitalized.isdigit():
                return capitalized
        
        # Fallback: Projeto Sem Nome
        return "Projeto Sem Nome"
    
    def extract_professionals_from_page(self, page_text: str) -> List[Dict]:
        """Extrai profissionais de uma p??gina espec??fica"""
        professionals = []
        
        # Buscar padr??o: Nome do profissional (geralmente em destaque)
        # Matr??cula: XXX Cargo: YYY
        
        # Padr??o 1: Buscar linha com "Matricula:" ou "Matr??cula:"
        matricula_pattern = r'Matr[??i]cula:\s*([A-Z]{2}\d+)'
        matriculas = re.findall(matricula_pattern, page_text, re.IGNORECASE)
        
        # Padr??o 2: Buscar nome antes da matr??cula
        # Formato comum: "Nome Completo\nMatricula: XXX"
        name_matricula_pattern = r'([A-Z??????????????????????][a-z??????????????????????]+(?:\s+[A-Z??????????????????????][a-z??????????????????????]+)+)\s+Matr[??i]cula:\s*([A-Z]{2}\d+)'
        name_matricula_matches = re.findall(name_matricula_pattern, page_text, re.IGNORECASE)
        
        for name, matricula in name_matricula_matches:
            professionals.append({
                'name': name.strip(),
                'registration': matricula.strip(),
                'page_text': page_text
            })
        
        return professionals
    
    def extract_activities_by_day(self, page_text: str) -> Dict[str, List[str]]:
        """
        Extrai atividades organizadas por dia da semana
        
        Estrat??gia:
        O PDF tem layout de tabela com colunas para cada dia.
        PyMuPDF l?? linearmente, ent??o distribu??mos as atividades
        sequencialmente pelos 5 dias da semana.
        """
        activities_by_day = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': []
        }
        
        # Extrair todas as atividades da p??gina
        all_activities = self._extract_all_activities_from_page(page_text)
        
        if not all_activities:
            return activities_by_day
        
        # Distribuir atividades sequencialmente pelos dias
        # Assumindo que o PDF lista atividades em ordem: segunda, ter??a, quarta, quinta, sexta
        days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
        # Calcular quantas atividades por dia (divis??o aproximada)
        activities_per_day = len(all_activities) / 5
        
        # Distribuir
        for i, activity in enumerate(all_activities):
            # Determinar a qual dia pertence esta atividade
            day_index = min(int(i / activities_per_day), 4)  # Max 4 (friday)
            day_key = days_list[day_index]
            activities_by_day[day_key].append(activity)
        
        return activities_by_day
    
    def _extract_all_activities_from_page(self, page_text: str) -> List[str]:
        """Extrai todas as atividades de uma p??gina"""
        activities = []
        
        # Lista de categorias conhecidas
        categories = [
            'Organiza????o Cadastral',
            'Teste de Funcionalidades',
            'Forma????o e Treinamento',
            'Elabora????o de Relat??rios',
            'Vistoria ?? Setores ou Unidades',
            'Suporte T??cnico',
            'Reuni??o',
            'Desenvolvimento',
            'Atendimento',
            'Manuten????o'
        ]
        
        # Estrat??gia: Split por marcadores de unidade e processar cada bloco
        # Marcadores: Sem Unidade, EMEIEF, EMEI, CREI
        unit_markers = ['Sem Unidade', 'EMEIEF', 'EMEI', 'CREI']
        
        # Dividir o texto em blocos usando os marcadores
        blocks = re.split(r'\n(?:Sem Unidade|EMEIEF[^\n]*|EMEI[^\n]*|CREI[^\n]*)\n', page_text)
        
        for block in blocks:
            # Para cada categoria, verificar se est?? presente neste bloco
            for category in categories:
                if category in block:
                    # Extrair texto ap??s a categoria
                    pattern = rf'{re.escape(category)}\s*\n\s*(.+?)(?=\n(?:{"|".join([re.escape(c) for c in categories])})|$)'
                    matches = re.findall(pattern, block, re.MULTILINE | re.DOTALL)
                    
                    for description in matches:
                        description = description.strip()
                        
                        # Remover bullet e espa??os extras
                        description = re.sub(r'^[\s]*', '', description)
                        description = re.sub(r'\s+', ' ', description).strip()
                        
                        # Pular se muito curta
                        if len(description) < 10:
                            continue
                        
                        activity_text = f"{category}: {description}"
                        
                        # Truncar se muito longa
                        if len(activity_text) > 250:
                            activity_text = activity_text[:247] + '...'
                        
                        activities.append(activity_text)
        
        # Remover duplicatas mantendo a ordem
        seen = set()
        unique_activities = []
        for act in activities:
            if act not in seen:
                seen.add(act)
                unique_activities.append(act)
        
        return unique_activities
    
    def _extract_activities_from_section(self, section_text: str) -> List[str]:
        """Extrai atividades de uma se????o de texto"""
        activities = []
        
        # Novo padr??o para o formato espec??fico do PDF:
        # Categoria (ex: "Organiza????o Cadastral")
        # Bullet "" + descri????o
        # "Sem Unidade" ou nome da unidade
        
        # Padr??o melhorado: captura categoria e descri????o
        # Ex: "Organiza????o Cadastral\n Card??pio da merenda..."
        pattern = r'([A-Z??????????????????????][^\n]{10,})\n\s*([^\n]{20,}?)(?:\nSem Unidade|\nEMEIEF|\nEMEI|\nCREI|\n[A-Z]{2,})'
        matches = re.findall(pattern, section_text, re.MULTILINE)
        
        for category, description in matches:
            # Limpar categoria e descri????o
            category = category.strip()
            description = description.strip()
            
            # Remover bullet "" se existir
            description = re.sub(r'^[\s]*', '', description).strip()
            
            # Formato: "Categoria: Descri????o"
            activity_text = f"{category}: {description}"
            
            # Limpar espa??os m??ltiplos
            activity_text = re.sub(r'\s+', ' ', activity_text)
            
            # Truncar descri????es muito longas
            if len(activity_text) > 200:
                activity_text = activity_text[:197] + '...'
            
            activities.append(activity_text)
        
        # Fallback: buscar linhas que come??am com bullet  ou categorias conhecidas
        if not activities:
            for cat in self.ACTIVITY_CATEGORIES:
                if cat in section_text:
                    # Extrair texto ap??s a categoria
                    pattern = rf'{cat}\s*\n\s*([^\n]+)'
                    matches = re.findall(pattern, section_text)
                    for match in matches:
                        clean_desc = re.sub(r'^[\s]*', '', match).strip()
                        if clean_desc and len(clean_desc) > 10:
                            activities.append(f"{cat}: {clean_desc[:150]}")
        
        return activities
    
    def parse_full_planning(self, registered_professionals: List[Dict]) -> Dict:
        """
        Faz o parsing completo do PDF com IA
        
        Args:
            registered_professionals: Lista de profissionais cadastrados no sistema
            
        Returns:
            Dict com todos os dados extra??dos estruturados
        """
        result = {            'project_name': self.extract_project_name(),            'week_info': self.extract_week_info(),
            'professionals': [],
            'alerts': []
        }
        
        # Processar cada p??gina (cada profissional geralmente est?? em uma p??gina)
        for page_text in self.pages_text:
            # Extrair profissionais desta p??gina
            page_professionals = self.extract_professionals_from_page(page_text)
            
            for prof_data in page_professionals:
                # Extrair atividades por dia
                activities_by_day = self.extract_activities_by_day(prof_data['page_text'])
                
                # Adicionar profissional com atividades (independente de estar cadastrado)
                prof_result = {
                    'name': prof_data['name'],
                    'registration': prof_data['registration'],
                    'monday': 'Presente',
                    'monday_activities': '\n'.join(activities_by_day['monday']),
                    'tuesday': 'Presente',
                    'tuesday_activities': '\n'.join(activities_by_day['tuesday']),
                    'wednesday': 'Presente',
                    'wednesday_activities': '\n'.join(activities_by_day['wednesday']),
                    'thursday': 'Presente',
                    'thursday_activities': '\n'.join(activities_by_day['thursday']),
                    'friday': 'Presente',
                    'friday_activities': '\n'.join(activities_by_day['friday'])
                }
                
                result['professionals'].append(prof_result)
        
        return result
