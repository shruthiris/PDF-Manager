from core.models import Document
from db.database import get_connection

class DocumentRepository:
    def __init__(self):
        pass

    def save_document(self, doc):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO documents (filename, filepath, thumbnail_path, tags, description, uploaded_date, total_pages)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        """, (doc.filename, doc.filepath, doc.thumbnail_path, doc.tags, doc.description, doc.total_pages))
        conn.commit()
        conn.close()

    def search_documents_tags(self, tags, date=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM documents"
            conditions = []
            params = []

            if tags:
                conditions.append("tags LIKE ?")
                params.append(f"%{tags}%")
            if date:
                conditions.append("uploaded_date = ?")
                params.append(date)

            if conditions:
                query += " WHERE " + " OR ".join(conditions)

            rows = cursor.execute(query, params).fetchall()
            documents = []
            for row in rows:
                document = Document(
                    filename=row["filename"],
                    filepath=row["filepath"],
                    thumbnail_path=row["thumbnail_path"],
                    tags=row["tags"],
                    description=row["description"],
                    uploaded_date=row["uploaded_date"],
                    total_pages=row["total_pages"],
                )
                document.id = row["id"]
                documents.append(document)
            return documents
        finally:
            conn.close()