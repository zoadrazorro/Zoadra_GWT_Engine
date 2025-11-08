"""
CONVERT DOCX TO MARKDOWN
========================
Extracts text from .docx and converts to markdown
"""

from pathlib import Path
from docx import Document

def docx_to_markdown(docx_path: str, output_path: str = None):
    """
    Convert .docx file to markdown
    
    Args:
        docx_path: Path to .docx file
        output_path: Optional output path (defaults to same name with .md)
    """
    docx_path = Path(docx_path)
    
    if not docx_path.exists():
        print(f"ERROR: {docx_path} not found!")
        return
    
    # Default output path
    if output_path is None:
        output_path = docx_path.with_suffix('.md')
    else:
        output_path = Path(output_path)
    
    print(f"Converting: {docx_path}")
    print(f"Output to: {output_path}")
    print()
    
    # Load document
    doc = Document(docx_path)
    
    # Extract text with basic markdown formatting
    markdown_lines = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            markdown_lines.append("")
            continue
        
        # Detect headings by style
        style = para.style.name.lower() if para.style and para.style.name else ""
        
        if 'heading 1' in style or 'title' in style:
            markdown_lines.append(f"# {text}")
        elif 'heading 2' in style:
            markdown_lines.append(f"## {text}")
        elif 'heading 3' in style:
            markdown_lines.append(f"### {text}")
        elif 'heading 4' in style:
            markdown_lines.append(f"#### {text}")
        else:
            markdown_lines.append(text)
    
    # Join and save
    markdown_content = '\n'.join(markdown_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"[SUCCESS] Converted to markdown!")
    print(f"Output: {output_path}")
    print(f"Size: {len(markdown_content)} characters")
    print()
    print("Preview:")
    print("="*80)
    print(markdown_content[:1000])
    print("...")
    print("="*80)


if __name__ == "__main__":
    docx_to_markdown("ETHICA_UNIVERSALIS_COMPLETE.docx")
