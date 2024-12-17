from database.connection import get_db_connection


def initialize_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        tables = [
            ('''
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            ''', 'authors'),
            ('''
                CREATE TABLE IF NOT EXISTS magazines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            ''', 'magazines'),
            ('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER,
                    magazine_id INTEGER,
                    FOREIGN KEY (author_id) REFERENCES authors (id),
                    FOREIGN KEY (magazine_id) REFERENCES magazines (id)
                )
            ''', 'articles')
        ]
        
        # Iterate over table definitions and create them if they don't exist
        for query, table in tables:
            print(f"Creating {table} table...")
            cursor.execute(query)

        conn.commit()
    print("Database tables created successfully.")
