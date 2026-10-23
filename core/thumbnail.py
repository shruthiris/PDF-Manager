import os
import pymupdf

THUMBNAIL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage", "thumbnails")

class ThumbnailManager:
    def save_thumbnail(self, filepath):
        doc = pymupdf.open(filepath)
        page = doc[0]  # Get the first page
        pixel = page.get_pixmap()        
        os.makedirs(THUMBNAIL_DIR, exist_ok=True)
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{os.path.splitext(os.path.basename(filepath))[0]}_thumbnail.png")
        pixel.save(thumbnail_path)
        doc.close()
        return thumbnail_path

    def total_pages(self, filepath):
        doc = pymupdf.open(filepath)
        pages_count = len(doc)
        doc.close()
        return pages_count