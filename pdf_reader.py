

import fitz  # PyMuPDF
import os

def extract_text_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        text_content = ""
        section_title = f"Page {page_num}"  # Default fallback
        max_font_size = 0

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        font_size = span["size"]

                        # Use largest font on page as title
                        if font_size > max_font_size and len(text.split()) <= 10 and text:
                            max_font_size = font_size
                            section_title = text

                        text_content += text + " "

        sections.append({
            "document": os.path.basename(pdf_path),
            "page": page_num,
            "section_title": section_title,
            "text": text_content.strip()
        })

    return sections
