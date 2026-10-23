import os
import pymupdf

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage", "pdf")

class PDFReader:
    def convert_pdf_to_images(self, pdf_path):
        doc = pymupdf.open(pdf_path)
        folder_name = os.path.splitext(os.path.basename(pdf_path))[0]
        images_dir = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        images_paths = []
        for i in range(len(doc)):
            page = doc.load_page(i)
            matrix = pymupdf.Matrix(2, 2)  # Scale factor for better resolution
            pix = page.get_pixmap(matrix=matrix)
            image_path = os.path.join(images_dir, f"page_{i + 1}.png")
            pix.save(image_path)
            images_paths.append(image_path)
        doc.close()  