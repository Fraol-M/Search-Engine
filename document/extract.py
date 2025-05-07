import pdfplumber

def extract_text_clean(pdf_path):
    all_text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + '\n'  # Keep newlines or spaces!
    return all_text
