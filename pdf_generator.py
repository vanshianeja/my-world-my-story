from fpdf import FPDF
import re

def clean_text(text):
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--',
        '\u2026': '...',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

class StoryPDF(FPDF):

    def __init__(self, title, genre, mood):
        super().__init__()
        self.story_title = title
        self.genre = genre
        self.mood = mood

    def header(self):
        # Genre and mood tag at top
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(140, 130, 200)
        self.cell(0, 10, f"{self.genre}  ·  {self.mood}", align="C")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"My World, My Story  ·  Page {self.page_no()}", align="C")

def generate_pdf(title, genre, mood, content):
    pdf = StoryPDF(title, genre, mood)
    pdf.set_margins(25, 20, 25)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    #Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 12, clean_text(title), align="C")
    pdf.ln(10)

    # Divider line
    pdf.set_draw_color(60, 60, 80)
    pdf.line(25, pdf.get_y(), 185, pdf.get_y())
    pdf.ln(12)

    # Story content
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)

    # Split into paracgraphs and add each
    paragraphs = content.split("\n")
    for para in paragraphs:
        para = para.strip()
        if para:
            pdf.multi_cell(0, 7, clean_text(para), align="J")
            pdf.ln(4)

    return bytes(pdf.output())
