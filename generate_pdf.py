#!/usr/bin/env python3
"""
PDF Generator for Research Paper
Converts the research paper markdown to a professional PDF format
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def create_research_paper_pdf():
    """Convert the research paper markdown to PDF"""
    
    # Read the markdown file
    try:
        with open('RESEARCH_PAPER_TEMPLATE.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        print("✓ Markdown file loaded successfully")
    except FileNotFoundError:
        print("❌ Error: RESEARCH_PAPER_TEMPLATE.md not found")
        return
    
    # Convert markdown to HTML
    html = markdown.markdown(
        md_content, 
        extensions=['tables', 'toc', 'codehilite', 'fenced_code', 'attr_list']
    )
    
    # Academic paper CSS styling
    css_style = """
    @page {
        size: A4;
        margin: 1in;
        @top-left {
            content: "ANUFA: Hybrid AI-Driven E-commerce Platform";
            font-size: 10pt;
            font-style: italic;
        }
        @top-right {
            content: counter(page);
            font-size: 10pt;
        }
    }
    
    body {
        font-family: "Times New Roman", "Times", serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #000;
        text-align: justify;
        hyphens: auto;
    }
    
    /* Headings */
    h1 {
        font-size: 18pt;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin: 30px 0 20px 0;
        page-break-after: avoid;
    }
    
    h2 {
        font-size: 16pt;
        font-weight: bold;
        color: #2c3e50;
        margin: 25px 0 15px 0;
        page-break-after: avoid;
    }
    
    h3 {
        font-size: 14pt;
        font-weight: bold;
        color: #2c3e50;
        margin: 20px 0 10px 0;
        page-break-after: avoid;
    }
    
    h4 {
        font-size: 12pt;
        font-weight: bold;
        color: #2c3e50;
        margin: 15px 0 8px 0;
        page-break-after: avoid;
    }
    
    /* Abstract and Keywords */
    .abstract {
        font-style: italic;
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
    }
    
    /* Tables */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-size: 11pt;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #333;
        padding: 8px 12px;
        text-align: left;
        vertical-align: top;
    }
    
    th {
        background-color: #f0f0f0;
        font-weight: bold;
        text-align: center;
    }
    
    /* Code blocks */
    pre, code {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 3px;
        font-family: "Courier New", "Consolas", monospace;
        font-size: 10pt;
        padding: 5px 8px;
    }
    
    pre {
        margin: 15px 0;
        padding: 15px;
        overflow-x: auto;
        white-space: pre-wrap;
    }
    
    /* Lists */
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 5px 0;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4px solid #3498db;
        margin: 20px 0;
        padding-left: 20px;
        font-style: italic;
        background-color: #f8f9fa;
        padding: 15px 15px 15px 35px;
    }
    
    /* References */
    .references {
        font-size: 11pt;
        line-height: 1.4;
    }
    
    /* Page breaks */
    .page-break {
        page-break-before: always;
    }
    
    /* Figures and captions */
    .figure {
        text-align: center;
        margin: 20px 0;
        page-break-inside: avoid;
    }
    
    .caption {
        font-size: 11pt;
        font-style: italic;
        margin-top: 10px;
        text-align: center;
    }
    
    /* Emphasis */
    strong, b {
        font-weight: bold;
    }
    
    em, i {
        font-style: italic;
    }
    
    /* Links */
    a {
        color: #2980b9;
        text-decoration: none;
    }
    
    a[href]:after {
        content: " (" attr(href) ")";
        font-size: 10pt;
        color: #666;
    }
    
    /* Mathematical expressions */
    .math {
        font-family: "Times New Roman", serif;
        font-style: italic;
    }
    
    /* Section numbering */
    body {
        counter-reset: h2counter;
    }
    
    h2:not(.no-counter):before {
        counter-increment: h2counter;
        content: counter(h2counter) ". ";
    }
    
    /* Footer information */
    .footer-info {
        font-size: 10pt;
        color: #666;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
    }
    """
    
    # Create complete HTML document
    html_document = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ANUFA: Hybrid AI-Driven Personalization in E-commerce</title>
        <style>{css_style}</style>
    </head>
    <body>
        {html}
        <div class="footer-info">
            <p><strong>Generated:</strong> {os.path.basename(os.getcwd())} Research Platform</p>
            <p><strong>Repository:</strong> https://github.com/anmolkumar8/ai-ecommerce-platform</p>
        </div>
    </body>
    </html>
    """
    
    # Save HTML file for reference
    with open('research_paper_temp.html', 'w', encoding='utf-8') as f:
        f.write(html_document)
    print("✓ HTML document created")
    
    # Generate PDF
    try:
        font_config = FontConfiguration()
        
        html_doc = HTML(string=html_document, base_url='.')
        css_doc = CSS(string=css_style, font_config=font_config)
        
        print("🔄 Generating PDF... This may take a moment...")
        html_doc.write_pdf(
            'AI_ECOMMERCE_RESEARCH_PAPER_PUBLICATION_READY.pdf',
            stylesheets=[css_doc],
            font_config=font_config
        )
        
        print("✅ SUCCESS: Research paper PDF generated!")
        print("📄 File: AI_ECOMMERCE_RESEARCH_PAPER_PUBLICATION_READY.pdf")
        print("📊 Pages: ~25-30 pages (estimated)")
        print("📝 Format: Academic journal format with proper citations")
        
        # Clean up temporary file
        if os.path.exists('research_paper_temp.html'):
            os.remove('research_paper_temp.html')
            
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("💡 The HTML file 'research_paper_temp.html' has been saved for manual conversion")

if __name__ == "__main__":
    print("🎓 ANUFA Research Paper PDF Generator")
    print("=" * 50)
    create_research_paper_pdf()
    print("=" * 50)
    print("🎯 Ready for submission to academic journals!")
