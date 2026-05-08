"""
PDF Generation Script for Hilltop Tea Documentation.

Converts all markdown documentation files to PDF using
python-markdown and WeasyPrint with premium styling.
"""

import os
import markdown
from weasyprint import HTML, CSS
from datetime import datetime


# Configuration
DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(DOCS_DIR, 'pdfs')

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Documentation files to convert
DOC_FILES = [
    'system_specification.md',
    'system_architecture.md',
    'flowchart.md',
    'system_documentation.md',
    'methodology.md',
    'tech_stack.md',
    'construction_decisions.md'
]

# Premium HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @top-center {{
                content: "HILLTOP TEA";
                font-family: 'Georgia', serif;
                font-size: 10pt;
                color: #1e3932;
            }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #6c757d;
            }}
        }}

        body {{
            font-family: 'Georgia', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }}

        .header {{
            text-align: center;
            border-bottom: 3px solid #1e3932;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .company-name {{
            font-size: 24pt;
            font-weight: bold;
            color: #1e3932;
            margin-bottom: 5px;
        }}

        .doc-title {{
            font-size: 18pt;
            color: #c9a96e;
            margin-top: 10px;
        }}

        .doc-meta {{
            text-align: center;
            font-size: 9pt;
            color: #6c757d;
            margin-top: 10px;
        }}

        h1 {{
            font-size: 18pt;
            color: #1e3932;
            border-bottom: 2px solid #c9a96e;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            page-break-before: always;
        }}

        h1:first-of-type {{
            page-break-before: avoid;
        }}

        h2 {{
            font-size: 14pt;
            color: #1e3932;
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        h3 {{
            font-size: 12pt;
            color: #2d5a4f;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        h4 {{
            font-size: 11pt;
            color: #2d5a4f;
            margin-top: 15px;
            margin-bottom: 8px;
        }}

        p {{
            margin-bottom: 12px;
            text-align: justify;
        }}

        ul, ol {{
            margin-bottom: 12px;
            padding-left: 30px;
        }}

        li {{
            margin-bottom: 6px;
        }}

        code {{
            font-family: 'Courier New', monospace;
            background-color: #f5f2eb;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10pt;
        }}

        pre {{
            background-color: #f5f2eb;
            border: 1px solid #e0d8c8;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            border: none;
            font-size: 9pt;
        }}

        blockquote {{
            border-left: 4px solid #c9a96e;
            padding-left: 15px;
            margin: 15px 0;
            color: #6c757d;
            font-style: italic;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }}

        th {{
            background-color: #1e3932;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #1e3932;
        }}

        td {{
            padding: 8px;
            border: 1px solid #ddd;
            vertical-align: top;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        a {{
            color: #1e3932;
            text-decoration: underline;
        }}

        hr {{
            border: none;
            border-top: 1px solid #c9a96e;
            margin: 20px 0;
        }}

        .toc {{
            background-color: #f5f2eb;
            border: 1px solid #e0d8c8;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }}

        .toc-title {{
            font-size: 14pt;
            font-weight: bold;
            color: #1e3932;
            margin-bottom: 15px;
            text-align: center;
        }}

        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}

        .toc li {{
            margin-bottom: 8px;
        }}

        .toc a {{
            color: #1e3932;
            text-decoration: none;
        }}

        .toc a:hover {{
            text-decoration: underline;
        }}

        .toc .toc-level-2 {{
            padding-left: 20px;
        }}

        .toc .toc-level-3 {{
            padding-left: 40px;
        }}

        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 9pt;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="company-name">HILLTOP TEA</div>
        <div class="doc-title">{title}</div>
        <div class="doc-meta">
            Generated on {date}
        </div>
    </div>

    {content}

    <div class="footer">
        <p>© {year} HILLTOP TEA. All rights reserved.</p>
        <p>Premium Tea, Precision Tracking</p>
    </div>
</body>
</html>
"""


def convert_markdown_to_html(md_file_path):
    """
    Convert a markdown file to HTML.

    Args:
        md_file_path: Path to the markdown file

    Returns:
        str: HTML content
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Configure markdown extensions
    extensions = [
        'tables',
        'fenced_code',
        'codehilite',
        'toc',
        'nl2br',
        'sane_lists'
    ]

    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=extensions,
        extension_configs={
            'codehilite': {
                'linenums': False,
                'css_class': 'highlight'
            },
            'toc': {
                'baselevel': 1,
                'title': 'Table of Contents'
            }
        }
    )

    return html_content


def generate_pdf(md_filename, html_content):
    """
    Generate PDF from HTML content.

    Args:
        md_filename: Original markdown filename
        html_content: HTML content to convert

    Returns:
        str: Path to generated PDF file
    """
    # Extract title from filename
    title = md_filename.replace('.md', '').replace('_', ' ').title()

    # Get current date
    current_date = datetime.now().strftime('%B %d, %Y')
    current_year = datetime.now().year

    # Apply HTML template
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        date=current_date,
        year=current_year
    )

    # Generate PDF
    pdf_filename = md_filename.replace('.md', '.pdf')
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    HTML(string=full_html).write_pdf(pdf_path)

    return pdf_path


def main():
    """Main function to convert all documentation files to PDF."""
    print("=" * 60)
    print("HILLTOP TEA - Documentation PDF Generator")
    print("=" * 60)
    print()

    converted_files = []
    failed_files = []

    for doc_file in DOC_FILES:
        md_path = os.path.join(DOCS_DIR, doc_file)

        if not os.path.exists(md_path):
            print(f"❌ File not found: {doc_file}")
            failed_files.append(doc_file)
            continue

        try:
            print(f"📄 Processing: {doc_file}")

            # Convert markdown to HTML
            html_content = convert_markdown_to_html(md_path)

            # Generate PDF
            pdf_path = generate_pdf(doc_file, html_content)

            print(f"✅ Generated: {pdf_path}")
            converted_files.append(pdf_path)

        except Exception as e:
            print(f"❌ Error processing {doc_file}: {str(e)}")
            failed_files.append(doc_file)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully converted: {len(converted_files)} files")
    print(f"❌ Failed: {len(failed_files)} files")
    print()
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()

    if converted_files:
        print("Generated PDFs:")
        for pdf_file in converted_files:
            print(f"  - {pdf_file}")

    if failed_files:
        print()
        print("Failed files:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")

    print()
    print("Done!")


if __name__ == '__main__':
    main()
