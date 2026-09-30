# pip intall PyMuPDF

import fitz
import os


def extract_pages_as_images(pdf_path, pages, output_path, dpi=300):

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_path, exist_ok=True)

    pdf = fitz.open(pdf_path)

    for page_num in pages:
        if page_num < 1 or page_num > len(pdf):
            print(f"Skipping invalid page number: {page_num}")
            continue
        page = pdf[page_num - 1]
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        image_path = os.path.join(
            output_path,
            f"page_{page_num}.png"
        )
        pix.save(image_path)
        print(f"Saved: {image_path}")
    pdf.close()


if __name__ == "__main__":
    pdf_path = r"D:\research\crime_united_states_2024_fbi_full.pdf"
    pages = [594 , 595, 596]
    output_path = r"D:\research\output"

    extract_pages_as_images(
        pdf_path,
        pages,
        output_path,
        dpi=300
    )