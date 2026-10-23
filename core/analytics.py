from db.database import get_connection

class AnalyticsService:   
    def record_page_visit(self, document_id, page_number):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pageVisits (document_id, page_number, visit_timestamp)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (document_id, page_number))
        conn.commit()
        conn.close()

    def get_document_analytics(self, document_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT page_number, visit_timestamp FROM pageVisits WHERE document_id = ?
        """, (document_id,))
        analytics_data = cursor.fetchall()
        conn.close()
        return analytics_data if analytics_data else 0
            
