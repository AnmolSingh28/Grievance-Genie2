import sqlite3
from typing import List, Dict, Optional

DB_FILENAME = "grievance_genie.db"

class ComplaintDB:
    def __init__(self, db_path=DB_FILENAME):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    complainer_name TEXT NOT NULL,
                    complainer_phonenum TEXT NOT NULL,
                    placeofissue TEXT,
                    complaint_detail TEXT NOT NULL,
                    category TEXT,
                    department TEXT,
                    status TEXT DEFAULT 'Registered',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def add_complaint(self, complaint: Dict):
        with self.conn:
            self.conn.execute('''
                INSERT INTO complaints (
                    citizen_name, contact, location, complaint_text,
                    category, department, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                complaint.get('complainer_name'),
                complaint.get('complainer_phonenum'),
                complaint.get('placeofissue'),
                complaint.get('complaint_detail'),
                complaint.get('category'),
                complaint.get('department'),
                complaint.get('status', 'Registered')
            ))

    def get_all_complaints(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM complaints ORDER BY id DESC')
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(cols, row)) for row in rows]

    def get_complaint_by_id(self, complaint_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
        row = cursor.fetchone()
        if row:
            cols = [col[0] for col in cursor.description]
            return dict(zip(cols, row))
        return None

    def close(self):
        self.conn.close()

# Example usage:
if __name__ == "__main__":
    db = ComplaintDB()
    db.add_complaint({
        'citizen_name': 'Test User',
        'contact': '1234567890',
        'location': 'Test Location',
        'complaint_text': 'Test complaint',
        'category': 'Test Category',
        'department': 'Test Department'
    })
    complaints = db.get_all_complaints()
    for c in complaints:
        print(c)
    db.close()
