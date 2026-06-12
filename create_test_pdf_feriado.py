from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os

# Criar PDF de teste com feriado
pdf_path = os.path.join('temp_uploads', 'teste_feriado_semana26.pdf')

doc = SimpleDocTemplate(pdf_path, pagesize=A4)
elements = []
styles = getSampleStyleSheet()

# T??tulo
title = Paragraph("<b>Planejamento Semanal - Escola Online Guar?? - Semana 26</b>", styles['Title'])
elements.append(title)
elements.append(Spacer(1, 0.5*cm))

# Per??odo
period = Paragraph("Per??odo: 17/06/2026 a 21/06/2026", styles['Normal'])
elements.append(period)
elements.append(Spacer(1, 0.5*cm))

# Dados Mara
elements.append(Paragraph("<b>Mara Coelho da Silva</b>", styles['Heading2']))
elements.append(Paragraph("Matrícula: MG38", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Segunda-feira (normal)
elements.append(Paragraph("<b>Segunda-feira</b>", styles['Heading3']))
elements.append(Paragraph("Organização Cadastral", styles['Normal']))
elements.append(Paragraph("Atualiza????o dos cadastros de alunos no sistema", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Ter??a-feira (FERIADO)
elements.append(Paragraph("<b>Ter??a-feira</b>", styles['Heading3']))
elements.append(Paragraph("Feriado Municipal", styles['Normal']))
elements.append(Paragraph("Ponto facultativo - Corpus Christi", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Quarta-feira (normal)
elements.append(Paragraph("<b>Quarta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Teste de Funcionalidades", styles['Normal']))
elements.append(Paragraph("Validação do portal do aluno", styles['Normal']))
elements.append(Paragraph("EMEIEF Central", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Quinta-feira (FOLGA)
elements.append(Paragraph("<b>Quinta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Folga programada", styles['Normal']))
elements.append(Paragraph("Folga compensat??ria do final de semana", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Sexta-feira (normal)
elements.append(Paragraph("<b>Sexta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Elaboração de Relatórios", styles['Normal']))
elements.append(Paragraph("Relatório mensal de atividades", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.5*cm))

# Dados Rian
elements.append(Paragraph("<b>Rian Gabriel Oliveira Miguel</b>", styles['Heading2']))
elements.append(Paragraph("Matrícula: MG37", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Segunda (normal)
elements.append(Paragraph("<b>Segunda-feira</b>", styles['Heading3']))
elements.append(Paragraph("Organização Cadastral", styles['Normal']))
elements.append(Paragraph("Levantamento de uso do sistema", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Ter??a (FERIADO - igual Mara)
elements.append(Paragraph("<b>Ter??a-feira</b>", styles['Heading3']))
elements.append(Paragraph("Feriado Municipal", styles['Normal']))
elements.append(Paragraph("Ponto facultativo - Corpus Christi", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Quarta (normal)
elements.append(Paragraph("<b>Quarta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Teste de Funcionalidades", styles['Normal']))
elements.append(Paragraph("Testes de integra????o", styles['Normal']))
elements.append(Paragraph("EMEI Norte", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Quinta (normal - diferente de Mara)
elements.append(Paragraph("<b>Quinta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Formação e Treinamento", styles['Normal']))
elements.append(Paragraph("Capacita????o de professores", styles['Normal']))
elements.append(Paragraph("CREI Sul", styles['Normal']))
elements.append(Spacer(1, 0.3*cm))

# Sexta (RECESSO)
elements.append(Paragraph("<b>Sexta-feira</b>", styles['Heading3']))
elements.append(Paragraph("Recesso escolar", styles['Normal']))
elements.append(Paragraph("Dia n??o letivo - planejamento pedag??gico", styles['Normal']))
elements.append(Paragraph("Sem Unidade", styles['Normal']))

doc.build(elements)
print(f'??? PDF criado: {pdf_path}')
print('\nConte??do:')
print('- Mara: Segunda (normal), Ter??a (FERIADO), Quarta (normal), Quinta (FOLGA), Sexta (normal)')
print('- Rian: Segunda (normal), Ter??a (FERIADO), Quarta (normal), Quinta (normal), Sexta (RECESSO)')
