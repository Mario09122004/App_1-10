import sqlite3

class Database:
    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.connect()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                year INTEGER,
                isbn INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def insert(self, title, author, year, isbn):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
            (title, author, year, isbn)
        )
        conn.commit()
        conn.close()

    def view_all(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        conn.close()
        return rows

    def search_entry(self, title="", author="", year="", isbn=""):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?",
            (title, author, year, isbn)
        )
        rows = cur.fetchall()
        conn.close()
        return rows

    def update(self, id, title, author, year, isbn):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(
            "UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
            (title, author, year, isbn, id)
        )
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=?", (id,))
        conn.commit()
        conn.close()

