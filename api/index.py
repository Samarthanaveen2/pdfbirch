from flask import Flask, send_file, make_response
from fpdf import FPDF
import random
import string
import io

app = Flask(__name__)

# --- PDF LOGIC ---
WORDS = ["strategy", "growth", "market", "value", "user", "product", "system", "data", "cloud", "AI", "project", "scale"]

def get_random_sentence():
    length = random.randint(10, 20)
    sentence = " ".join(random.choice(WORDS) for _ in range(length))
    return sentence.capitalize() + "."

def generate_messy_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for page in range(10):
        pdf.add_page()
        for _ in range(20):
            family = random.choice(['Arial', 'Times', 'Courier'])
            style = random.choice(['', 'B', 'I'])
            size = random.randint(10, 14)
            pdf.set_font(family, style, size)
            pdf.multi_cell(0, 10, get_random_sentence(), align='L')

            # Anti-Detector Noise
            pdf.set_text_color(255, 255, 255)
            pdf.set_font('Arial', '', 6)
            noise = ''.join(random.choices(string.ascii_letters, k=10))
            pdf.cell(0, 5, noise, ln=1)
            pdf.set_text_color(0, 0, 0)

    pdf_string = pdf.output(dest='S')
    buffer = io.BytesIO(pdf_string.encode('latin-1'))
    buffer.seek(0)
    return buffer

# --- VERCEL HANDLER ---
@app.route('/api/download')
def download():
    try:
        pdf_buffer = generate_messy_pdf()
        filename = f"Dataset_{random.randint(1000,9999)}.pdf"
        response = make_response(send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf'))
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# This line is critical for Vercel
app.debug = True