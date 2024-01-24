"""
Reference
https://cloud.tencent.com/developer/article/1778801
"""
# PyPDF2==3.0.1
#reportlab==4.0.9
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from os import remove
import argparse
from pathlib import Path

def create_watermark(content, num_per_row, num_of_row):
    file_name = "mark.pdf"
    c = canvas.Canvas(file_name, pagesize=(22*cm, 28*cm))
    c.translate(10*cm, 5*cm)

    c.setFont("Helvetica", 20)
    c.setStrokeColorRGB(0, 1, 0)
    c.setFillColorRGB(0, 1, 0)
    c.rotate(30)
    c.setFillColorRGB(0, 0, 0, 0.1)
    for i in range(num_per_row):
        for j in range(num_of_row):
            a=10*(i-1)
            b=5*(j-2)
            c.drawString(a*cm, b*cm, content)
            c.setFillAlpha(0.1)
    c.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    
    pdf_output = PdfWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfReader(input_stream, strict=False)

    pageNum = len(pdf_input.pages)

    pdf_watermark = PdfReader(open(pdf_file_mark, 'rb'), strict=False)
    for i in range(pageNum):
        page = pdf_input.pages[i]
        page.merge_page(pdf_watermark.pages[0])
        page.compress_content_streams() 
        pdf_output.add_page(page)
    pdf_output.write(open(pdf_file_out, 'wb'))
    remove('mark.pdf')
    input_stream.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pdf-input", 
                        help="The path to the input pdf", 
                        required=True)
    parser.add_argument("-n", "--num-per-row", 
                        help="The number of water mark per row", 
                        type=int,
                        default=1)
    parser.add_argument("-r", "--num-of-row", 
                        help="The number of row per page", 
                        type=int,
                        default=8)
    args = parser.parse_args()

    pdf_file_in = args.pdf_input
    num_per_row = args.num_per_row
    num_of_row = args.num_of_row
    pdf_file_in = Path(pdf_file_in)
    pdf_file_out = pdf_file_in.stem + "_watermarked" + pdf_file_in.suffix
    pdf_file_out = pdf_file_in.with_name(pdf_file_out)
    pdf_file_mark = create_watermark('For background check only', num_per_row, num_of_row)
    add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)
    