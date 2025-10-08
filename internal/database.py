import apsw  # или from pysqlite3 import dbapi2 as sqlite3
import sqlite_vec
from array import array

def create_table_query():
    return """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        embedding VECTOR(1536),
        uuid TEXT
    )
    """

def to_f32_blob(vec: list[float]) -> bytes:
    # проверим размер (опционально)
    if len(vec) != 1536:
        raise ValueError(f"Embedding must have 1536 dims, got {len(vec)}")
    return array('f', vec).tobytes()  # float32 → bytes

class Database:
    conn = None

    def __init__(self, db_path="symptoms.db"):
        self.conn = apsw.Connection(db_path)
        if hasattr(self.conn, "enableloadextension"):
            self.conn.enableloadextension(True)
        elif hasattr(self.conn, "enable_load_extension"):
            self.conn.enable_load_extension(True)

        sqlite_vec.load(self.conn)

        cur = self.conn.cursor()
        cur.execute(create_table_query())
        cur.close()

    def add_vector(self, name: str, vector: list[float], uuid: str):
        blob = to_f32_blob(vector)
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO items (name, embedding, uuid) VALUES (?, ?, ?)",
            (name, blob, uuid),
        )
        cur.close()

    def find_closest(self, vector: list[float], limit=5):
        blob = to_f32_blob(vector)  # float32 -> bytes
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id,
                   name,
                   uuid,
                   vec_distance_L2(embedding, ?) AS distance
            FROM items
            ORDER BY distance LIMIT ?
            """,
            (blob, int(limit)),
        )
        rows = list(cur)
        cur.close()
        return rows

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

