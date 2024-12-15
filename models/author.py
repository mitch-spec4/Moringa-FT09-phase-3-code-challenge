class Author:
    def __init__(self, author_id, author_name):
        self._author_id = author_id
        self._author_name = author_name

    @property
    def author_id(self):
        return self._author_id

    @property
    def author_name(self):
        return self._author_name

    @author_name.setter
    def author_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Author's name must be a string.")
        if len(value) == 0:
            raise ValueError("Author's name cannot be empty.")
        if hasattr(self, '_author_name'):
            raise AttributeError("Author's name cannot be modified after initialization.")
        self._author_name = value

    def save_author(self, cursor):
        # Inserting a new author
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._author_name,))
        self._author_id = cursor.lastrowid

    @classmethod
    def fetch_all_authors(cls, cursor):
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(author_id=row[0], author_name=row[1]) for row in authors_data]

    def get_associated_articles(self, cursor):
        # Fetching all articles linked to the author
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._author_id,))
        articles_data = cursor.fetchall()
        return articles_data

    def get_associated_magazines(self, cursor):
        # Fetching all magazines linked to the author via articles
        cursor.execute("""
            SELECT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._author_id,))
        magazines_data = cursor.fetchall()
        return magazines_data
