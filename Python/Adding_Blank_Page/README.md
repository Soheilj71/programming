# PDF Note Page Generator

## 📌 Purpose
This script allows you to add a blank note page next to every page of an existing PDF.
It is useful for printing study materials, books, or research papers with extra space for handwritten or digital annotations.

## 🛠 How It Works

The script:
	1.	Reads an input PDF file using pypdf.
	2.	Creates a blank PDF page of the same size for each page using ReportLab.
	3.	Combines the original PDF page (left) and the blank page (right) into a single double-width page.
	4.	Writes all combined pages into a new output PDF.

This way, every page in your output PDF has a dedicated note section.

## 📂 File Structure

<pre> 
convert.py        # Main Python script
README.md         # This file
input.pdf         # Your source PDF file (you provide this)
output_with_notes.pdf  # The generated PDF with note pages
</pre>

## 🚀 Usage

### 1. Install Dependencies

Make sure you have Python installed. Then, install the required libraries:

```bash
pip install pypdf reportlab
```

### 2. Run the Script

Place your input PDF in the same folder as convert.py or provide the path.
Edit the script variables:
<pre>
input_pdf_path = "input.pdf"          # Change this to your PDF file
output_pdf_path = "output_with_notes.pdf"  # Change this if you want a custom name
</pre>

Run the script:
```python
python convert.py
```
### 3. Output

The script generates a new PDF file with every original page on the left and a blank note page on the right:
<pre>
✅ Done! Saved as: output_with_notes.pdf
</pre>

## 📝 Example

If your input PDF has 10 pages, the output will also have 10 pages, but each will be double width (page + blank notes area).


## 🔧 Customization

You can modify:
- input_pdf_path → to select a different PDF file.
- output_pdf_path → to change the output filename.
- Page sizes can be adjusted by modifying width or height before creating the blank note page.
- You can add lines or a grid to the blank note page by modifying the create_blank_page function (using ReportLab drawing tools).

## ⚠️ Notes
- Works best with PDFs that use a standard page size (A4 or Letter).
- For very large PDFs, the process may take longer.
- The output file size will increase because each page is duplicated in width.
