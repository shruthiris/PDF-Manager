class Document:
    def __init__(self, filename, filepath, thumbnail_path, tags, description, uploaded_date, total_pages):
        self.id = None  # ID will be set when the document is saved to the database
        self.filename = filename
        self.filepath = filepath
        self.thumbnail_path = thumbnail_path
        self.tags = tags
        self.description = description
        self.uploaded_date = uploaded_date
        self.total_pages = total_pages