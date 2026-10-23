import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdfpath = os.path.join(BASE_DIR, "storage", "pdf")

class FileManager:
    def save_file(self, filename, filepath):
        os.makedirs(pdfpath, exist_ok=True)
        name, extension = os.path.splitext(os.path.basename(filename))
        filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"
        destination_path = os.path.join(pdfpath, filename)

        with open(destination_path, "wb") as destination:
            destination.write(filepath.getvalue())
            
        return destination_path