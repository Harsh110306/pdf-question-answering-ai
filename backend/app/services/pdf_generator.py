from fpdf import FPDF
from app.models.domain import ChatMessage
from typing import List

def create_chat_pdf(messages: List[ChatMessage], output_path: str):
    pdf = FPDF()
    pdf.add_page()
    
    # Use built-in Helvetica which supports basic Latin
    pdf.set_font("Helvetica", size=12)
    
    for msg in messages:
        role = "User" if msg.role == "user" else "AI"
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, txt=f"{role}:", align='L')
        pdf.ln(8)
        
        pdf.set_font("Helvetica", size=11)
        # Replace unencodable characters for basic latin font
        safe_text = msg.content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=safe_text)
        pdf.ln(5)
        
    pdf.output(output_path)
