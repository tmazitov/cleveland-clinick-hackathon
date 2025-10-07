import sqlite3
import sqlite_vector

def create_table_query():
    return """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        embedding VECTOR(1536)
    )
    """

class Database:
    conn:sqlite3.Connection = None

    def __init__(self, db_path="symptoms.db"):
        self.conn = sqlite3.connect(db_path)
        sqlite_vector.load(self.conn)
        
    def add_vector(self, name:str, vector:list[float]):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO items (name, embedding) VALUES (?, ?)", (name, vector))
        self.conn.commit()
        cursor.close()

    def find_closest(self, vector:list[float], limit=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, embedding <-> ? AS distance FROM items ORDER BY distance LIMIT ?", (vector, limit))
        results = cursor.fetchall()
        cursor.close()
        return results

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None