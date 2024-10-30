from PyPDF2 import PdfReader
import docx
import io
def parse_resume(filename, content):
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(content)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(content)
    return content  # If it's plain text, return the content as-is

def extract_text_from_pdf(content):
    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(content):
    doc = docx.Document(io.BytesIO(content))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)
