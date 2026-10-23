from db.repository import DocumentRepository
from datetime import datetime
from core.file_manager import FileManager
from core.thumbnail import ThumbnailManager
from core.reader import PDFReader
from core.models import Document
from core.analytics import AnalyticsService

import os

class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()
        self.analytics_service = AnalyticsService()
        self.file_manager = FileManager()
        self.thumbnail_manager = ThumbnailManager()
        

    def upload_document(self, filename, filepath, tags, description):
        # Save the file
        file_path = self.file_manager.save_file(filename, filepath)
        thumbnail_path = self.thumbnail_manager.save_thumbnail(file_path)
        total_pages = self.thumbnail_manager.total_pages(file_path)
        PDFReader().convert_pdf_to_images(file_path)
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc = Document(
            filename=filename,
            filepath=file_path,
            thumbnail_path=thumbnail_path,
            tags=tags,
            description=description,
            uploaded_date=upload_date,
            total_pages=total_pages
        )   
        self.repository.save_document(doc)

    def search_documents_tags(self, tags):
        return self.repository.search_documents_tags(tags)

    def view_analytics(self, document_id):
        return self.analytics_service.get_document_analytics(document_id)
        pass