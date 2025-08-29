# Written by Soheil Jamali
# Email: soheil.jamali.dev@gmail.com, sjamali@uark.edu

# ==============================
# PDF MERGING SCRIPT WITH NOTES
# ==============================
# This script takes an input PDF and generates a new PDF where
# each original page is placed on the left, and a blank page
# for notes is added on the right.

from pypdf import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO

# ========== USER INPUT ==========
input_pdf_path = "input.pdf"  # Path to the original PDF
output_pdf_path = "output_with_notes.pdf"  # Path to save the new PDF

# Load the original PDF
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

def create_blank_page(width, height):
    """
    Create a blank PDF page of the given size.
    This will be used for the note-taking area.
    
    Args:
        width (float): Width of the page.
        height (float): Height of the page.
    
    Returns:
        PageObject: A blank PDF page.
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.showPage()  # Finalize the blank page
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

# Iterate through every page of the input PDF
for page in reader.pages:
    width = float(page.mediabox.width)   # Get the width of the original page
    height = float(page.mediabox.height) # Get the height of the original page

    # Create a blank page (same size as the original page)
    blank_page = create_blank_page(width, height)

    # Create a new combined page (double width: original + blank note page)
    new_page = PageObject.create_blank_page(width=width * 2, height=height)

    # Place the original page on the left
    new_page.merge_page(page)

    # Place the blank note page on the right (translated by original page width)
    new_page.merge_translated_page(blank_page, tx=width, ty=0)

    # Add this combined page to the PDF writer
    writer.add_page(new_page)

# Write the new PDF file
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print("✅ Done! Saved as:", output_pdf_path)
