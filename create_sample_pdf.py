"""
Script para gerar PDF de teste do planejamento semanal
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def create_sample_planning_pdf(filename="exemplo_planejamento_semana25.pdf"):
    """Cria um PDF de exemplo de planejamento semanal"""
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # TÜtulo
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1A237E'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    elements.append(Paragraph("Planejamento Semanal", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Info geral
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    )
    
    elements.append(Paragraph("<b>Projeto:</b> Educaita", info_style))
    elements.append(Paragraph("<b>Semana 25</b>", info_style))
    elements.append(Paragraph("<b>PerÜodo:</b> 15/06/2026 a 19/06/2026", info_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabela de profissionais
    data = [
        ['Profissional', 'Matrícula', 'Segunda\n15/06', 'TerÜa\n16/06', 'Quarta\n17/06', 'Quinta\n18/06', 'Sexta\n19/06'],
        ['AndrÜ Luiz GuimarÜes', 'MI34', 'Presente', 'Presente', 'Feriado', 'Presente', 'Presente'],
        ['Gustavo Zuim', 'MI10', 'Presente', 'Presente', 'Feriado', 'Presente', 'Presente'],
        ['Nathani', 'MI11', 'Presente', 'Presente', 'Feriado', 'Folga', 'Presente'],
    ]
    
    table = Table(data, colWidths=[2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A148C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Observações
    obs_style = ParagraphStyle(
        'Obs',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        spaceAfter=6
    )
    
    elements.append(Paragraph("<b>Observações:</b>", info_style))
    elements.append(Paragraph("Ü? Quarta-feira (17/06): Corpus Christi - Feriado Nacional", obs_style))
    elements.append(Paragraph("Ü? Nathani: Folga compensatÜria na quinta-feira", obs_style))
    elements.append(Paragraph("Ü? Todos os profissionais devem estar presentes nos demais dias", obs_style))
    
    # Build PDF
    doc.build(elements)
    print(f"PDF de exemplo criado: {filename}")

if __name__ == '__main__':
    # Instalar reportlab antes: pip install reportlab
    create_sample_planning_pdf()
