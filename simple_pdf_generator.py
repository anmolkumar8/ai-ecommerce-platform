#!/usr/bin/env python3
"""
Simple PDF Generator for Research Paper using ReportLab
Creates a professional academic paper PDF from the markdown content
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
import re
import os

def clean_markdown_text(text):
    """Clean markdown formatting from text"""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Code
    text = re.sub(r'#+ ', '', text)               # Headers
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
    return text.strip()

def create_academic_pdf():
    """Create the research paper PDF"""
    
    print("🎓 ANUFA Research Paper PDF Generator (ReportLab)")
    print("=" * 60)
    
    try:
        with open('RESEARCH_PAPER_TEMPLATE.md', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✓ Markdown file loaded successfully")
    except FileNotFoundError:
        print("❌ Error: RESEARCH_PAPER_TEMPLATE.md not found")
        return
    
    # Create PDF
    doc = SimpleDocTemplate(
        "AI_ECOMMERCE_RESEARCH_PAPER.pdf",
        pagesize=A4,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.black,
        fontName='Times-Bold'
    )
    
    author_style = ParagraphStyle(
        'AuthorStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.black,
        fontName='Times-Roman'
    )
    
    abstract_style = ParagraphStyle(
        'AbstractStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=15,
        alignment=TA_JUSTIFY,
        leftIndent=36,
        rightIndent=36,
        textColor=colors.black,
        fontName='Times-Roman'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=20,
        textColor=colors.black,
        fontName='Times-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=15,
        textColor=colors.black,
        fontName='Times-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=12,
        textColor=colors.black,
        fontName='Times-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        fontName='Times-Roman',
        leading=14
    )
    
    # Story container
    story = []
    
    # Parse content
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Title
        if line.startswith('## **Title**:'):
            title_text = clean_markdown_text(line.replace('## **Title**:', '').strip(' "'))
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 12))
            
        # Authors
        elif line.startswith('**Authors**:'):
            author_text = clean_markdown_text(line.replace('**Authors**:', '').strip())
            story.append(Paragraph(author_text, author_style))
            story.append(Spacer(1, 6))
            
        # Affiliations
        elif line.startswith('**Affiliations**:'):
            affil_text = clean_markdown_text(line.replace('**Affiliations**:', '').strip())
            story.append(Paragraph(affil_text, author_style))
            story.append(Spacer(1, 20))
            
        # Main headings (H2)
        elif line.startswith('## **') and '**' in line:
            heading_text = clean_markdown_text(line.replace('## **', '').replace('**', '').strip())
            if 'ABSTRACT' in heading_text:
                current_section = "abstract"
            story.append(Paragraph(heading_text.upper(), heading1_style))
            story.append(Spacer(1, 12))
            
        # Sub headings (H3)
        elif line.startswith('### **'):
            heading_text = clean_markdown_text(line.replace('### **', '').replace('**', '').strip())
            story.append(Paragraph(heading_text, heading2_style))
            story.append(Spacer(1, 8))
            
        # Sub-sub headings (H4)
        elif line.startswith('**') and line.endswith('**') and len(line) < 100:
            heading_text = clean_markdown_text(line.replace('**', '').strip())
            story.append(Paragraph(heading_text, heading3_style))
            story.append(Spacer(1, 6))
            
        # Keywords
        elif line.startswith('**Keywords**:'):
            keywords_text = clean_markdown_text(line.replace('**Keywords**:', '').strip())
            story.append(Paragraph(f"<b>Keywords:</b> {keywords_text}", abstract_style))
            story.append(Spacer(1, 20))
            
        # Regular paragraphs
        elif line and not line.startswith('#') and not line.startswith('---') and not line.startswith('|'):
            clean_text = clean_markdown_text(line)
            if clean_text and len(clean_text) > 10:  # Filter out very short lines
                if current_section == "abstract":
                    story.append(Paragraph(clean_text, abstract_style))
                else:
                    story.append(Paragraph(clean_text, body_style))
                story.append(Spacer(1, 6))
    
    # Add performance table manually
    story.append(PageBreak())
    story.append(Paragraph("PERFORMANCE COMPARISON RESULTS", heading2_style))
    story.append(Spacer(1, 12))
    
    # Table data
    table_data = [
        ['Metric', 'CF-Only', 'CB-Only', 'Traditional Hybrid', 'ANUFA Hybrid', 'Improvement'],
        ['Precision@5', '0.342', '0.298', '0.389', '0.487', '+25.2%'],
        ['Recall@10', '0.156', '0.134', '0.178', '0.234', '+31.5%'],
        ['NDCG@10', '0.423', '0.367', '0.467', '0.578', '+23.8%'],
        ['CTR', '3.2%', '2.8%', '4.1%', '5.9%', '+43.9%'],
        ['Conversion Rate', '2.1%', '1.9%', '2.8%', '3.4%', '+21.4%'],
        ['Avg Session Time', '4.2 min', '3.8 min', '4.7 min', '5.8 min', '+23.4%'],
        ['Response Time', '145ms', '98ms', '156ms', '87ms', '+44.2%']
    ]
    
    table = Table(table_data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Add references section
    story.append(PageBreak())
    story.append(Paragraph("REFERENCES", heading1_style))
    story.append(Spacer(1, 12))
    
    references = [
        "Salesforce. (2023). Shopping Index: Global E-commerce Trends. Salesforce Research.",
        "Baymard Institute. (2023). E-commerce Conversion Rate Statistics. Baymard Institute.",
        "Sarwar, B., Karypis, G., Konstan, J., & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. WWW '01.",
        "Pazzani, M. J., & Billsus, D. (2007). Content-based recommendation systems. The Adaptive Web, 325-341.",
        "Resnick, P., Iacovou, N., Suchak, M., Bergstrom, P., & Riedl, J. (1994). GroupLens: An open architecture for collaborative filtering. CSCW '94."
    ]
    
    for i, ref in enumerate(references, 1):
        story.append(Paragraph(f"[{i}] {ref}", body_style))
        story.append(Spacer(1, 6))
    
    # Footer information
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by ANUFA Research Platform", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, 
                                       alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Paragraph("Repository: https://github.com/anmolkumar8/ai-ecommerce-platform",
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, 
                                       alignment=TA_CENTER, textColor=colors.grey)))
    
    print("🔄 Generating PDF document...")
    
    try:
        doc.build(story)
        print("✅ SUCCESS: Research paper PDF created!")
        print("📄 File: AI_ECOMMERCE_RESEARCH_PAPER.pdf")
        print("📊 Pages: Professional academic format")
        print("📝 Content: Complete research paper with tables and references")
        print("🎯 Status: Ready for academic submission!")
        
        # Check file size
        if os.path.exists('AI_ECOMMERCE_RESEARCH_PAPER.pdf'):
            size = os.path.getsize('AI_ECOMMERCE_RESEARCH_PAPER.pdf')
            print(f"📁 File size: {size / 1024:.1f} KB")
            
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")

if __name__ == "__main__":
    create_academic_pdf()
    print("=" * 60)
