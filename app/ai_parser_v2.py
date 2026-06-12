"""
Parser de PDF SUPER ROBUSTO - Versão 2.0
Extrai dados mesmo de PDFs mal formatados
"""
import fitz
import re
from datetime import datetime
from typing import Dict, List

class PlanningAIParser:
    """Parser ultra-robusto para qualquer formato de PDF"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = self.extract_text()
        self.pages_text = self.extract_pages_text()
        self.lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        
    def extract_text(self) -> str:
        """Extrai todo o texto do PDF"""
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_pages_text(self) -> List[str]:
        """Extrai texto de cada página"""
        doc = fitz.open(self.pdf_path)
        pages = [page.get_text() for page in doc]
        doc.close()
        return pages
    
    def extract_project_name(self) -> str:
        """Extrai nome do projeto com múltiplas estratégias"""
        text = '\n'.join(self.pages_text[:3])  # Primeiras 3 páginas
        
        # Estratégia 1: "Projeto: NOME" ou "Projeto NOME"
        patterns = [
            r'Projeto\s*[:\-]?\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][^\n]{5,80})',
            r'PROJECT\s*[:\-]?\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][^\n]{5,80})',
            r'PROJETO\s*[:\-]?\s*([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][^\n]{5,80})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                name = re.sub(r'[\s\-_:;]+$', '', name)  # Limpar fim
                if len(name) > 3 and not name.lower().startswith(('semana', 'matricula', 'cargo')):
                    return name
        
        # Estratégia 2: Primeira linha em maiúsculas que parece título
        for line in self.lines[:30]:
            if (len(line) > 5 and len(line) < 100 and 
                line[0].isupper() and 
                not line.lower().startswith(('matricula', 'cargo', 'semana', 'segunda', 'terça'))):
                # Verificar se tem pelo menos 2 palavras
                words = line.split()
                if len(words) >= 2:
                    return line.strip()
        
        # Estratégia 3: Do nome do arquivo
        import os
        filename = os.path.basename(self.pdf_path)
        clean_name = re.sub(r'\d{8}_\d{6}_', '', filename)  # Remove timestamp
        clean_name = re.sub(r'\.pdf$', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'planejamento[_\s\-]*', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'semana[_\s\-]*\d+', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[_\-]', ' ', clean_name)
        
        if clean_name and len(clean_name) > 3:
            return ' '.join(word.capitalize() for word in clean_name.split())
        
        return "Projeto Importado"
    
    def extract_week_info(self) -> Dict:
        """Extrai informações da semana"""
        result = {'week_label': None, 'dates': []}
        
        # Buscar "Semana XX" ou "SEMANA XX"
        week_match = re.search(r'semana\s+(\d+)', self.text, re.IGNORECASE)
        if week_match:
            result['week_label'] = f"Semana {week_match.group(1)}"
        
        # Buscar datas: dd/mm/yyyy, dd/mm/yy, dd-mm-yyyy
        date_patterns = [
            r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b',
        ]
        
        parsed_dates = []
        for pattern in date_patterns:
            for day, month, year in re.findall(pattern, self.text):
                try:
                    if len(year) == 2:
                        year = '20' + year
                    date_obj = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
                    if date_obj not in parsed_dates:
                        parsed_dates.append(date_obj)
                except:
                    pass
        
        if parsed_dates:
            result['dates'] = sorted(parsed_dates)
        
        return result
    
    def extract_professionals_from_page(self, page_text: str) -> List[Dict]:
        """Extrai profissionais com MÚLTIPLAS estratégias"""
        professionals = []
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        
        # Estratégia 1: Buscar "Matrícula: XXXX" e pegar nome antes
        for i, line in enumerate(lines):
            # Buscar matrículas em vários formatos
            mat_patterns = [
                r'Matr[íi]cula\s*[:\-]?\s*([A-Z]{1,3}\d+)',
                r'Matricula\s*[:\-]?\s*([A-Z]{1,3}\d+)',
                r'Mat\s*[:\-]?\s*([A-Z]{1,3}\d+)',
                r'\b([A-Z]{2}\d{4,})\b',  # Padrão direto: AB1234
            ]
            
            for pattern in mat_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    matricula = match.group(1).upper()
                    
                    # Tentar pegar nome nas linhas anteriores
                    nome = None
                    for j in range(max(0, i-5), i):
                        candidate = lines[j]
                        # Nome deve ter pelo menos 2 palavras, começar com maiúscula
                        if (len(candidate) > 5 and 
                            candidate[0].isupper() and 
                            len(candidate.split()) >= 2 and
                            not re.search(r'Matr[íi]cula|Cargo|Função|Semana', candidate, re.IGNORECASE)):
                            nome = candidate
                            break
                    
                    if not nome:
                        # Se não achou nome antes, buscar depois
                        for j in range(i+1, min(len(lines), i+3)):
                            candidate = lines[j]
                            if (len(candidate) > 5 and 
                                candidate[0].isupper() and 
                                len(candidate.split()) >= 2 and
                                not re.search(r'Matr[íi]cula|Cargo|Função', candidate, re.IGNORECASE)):
                                nome = candidate
                                break
                    
                    if nome:
                        # Limpar nome
                        nome = re.sub(r'\s+', ' ', nome).strip()
                        professionals.append({
                            'name': nome,
                            'registration': matricula,
                            'page_text': page_text
                        })
                        break
        
        # Estratégia 2: Se não encontrou nada, buscar padrões de nome + matrícula juntos
        if not professionals:
            # Pattern: "João da Silva AB1234"
            pattern = r'([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+(?:\s+(?:da|de|do|dos|das)?\s*[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+)+)\s+([A-Z]{2}\d+)'
            matches = re.findall(pattern, page_text)
            for name, mat in matches:
                professionals.append({
                    'name': name.strip(),
                    'registration': mat.strip(),
                    'page_text': page_text
                })
        
        # Remover duplicatas
        seen = set()
        unique = []
        for p in professionals:
            key = (p['name'].lower(), p['registration'])
            if key not in seen:
                seen.add(key)
                unique.append(p)
        
        return unique
    
    def extract_activities_simple(self, page_text: str) -> str:
        """Extrai atividades de forma simples - tudo que parece atividade"""
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        activities = []
        
        # Palavras-chave que indicam atividades
        keywords = ['organização', 'teste', 'formação', 'treinamento', 'elaboração', 
                   'relatório', 'vistoria', 'suporte', 'reunião', 'desenvolvimento',
                   'atendimento', 'manutenção', 'análise', 'documentação']
        
        for line in lines:
            line_lower = line.lower()
            # Se linha tem palavra-chave E tem tamanho razoável
            if any(kw in line_lower for kw in keywords) and 10 < len(line) < 200:
                # Limpar
                clean = re.sub(r'^\s*[\•\-\*]\s*', '', line)  # Remove bullets
                clean = re.sub(r'\s+', ' ', clean).strip()
                if clean and not clean.startswith(('Semana', 'Matrícula', 'Cargo')):
                    activities.append(clean)
        
        return '\n'.join(activities[:10])  # Máximo 10 atividades
    
    def parse_full_planning(self, registered_professionals: List[Dict]) -> Dict:
        """Parse completo do PDF"""
        result = {
            'project_name': self.extract_project_name(),
            'week_info': self.extract_week_info(),
            'professionals': [],
            'alerts': []
        }
        
        # Processar cada página
        for page_num, page_text in enumerate(self.pages_text):
            page_professionals = self.extract_professionals_from_page(page_text)
            
            for prof in page_professionals:
                # Extrair atividades simples (sem dividir por dia - apenas listar tudo)
                all_activities = self.extract_activities_simple(page_text)
                
                # Criar profissional com atividades distribuídas nos 5 dias
                prof_result = {
                    'name': prof['name'],
                    'registration': prof['registration'],
                }
                
                # Dividir atividades entre os 5 dias
                activity_lines = [a for a in all_activities.split('\n') if a]
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
                acts_per_day = max(1, len(activity_lines) // 5)
                
                for i, day in enumerate(days):
                    start_idx = i * acts_per_day
                    end_idx = start_idx + acts_per_day if i < 4 else len(activity_lines)
                    day_acts = activity_lines[start_idx:end_idx]
                    
                    prof_result[day] = 'Presente'
                    prof_result[f'{day}_activities'] = '\n'.join(day_acts) if day_acts else ''
                
                result['professionals'].append(prof_result)
        
        # Se não encontrou nenhum profissional
        if not result['professionals']:
            result['alerts'].append('ALERTA: Nenhum profissional detectado no PDF. Verifique se o formato está correto.')
            # Adicionar informações de debug
            result['debug_info'] = {
                'total_text_length': len(self.text),
                'first_100_chars': self.text[:100],
                'lines_count': len(self.lines),
                'pages_count': len(self.pages_text)
            }
        
        return result
