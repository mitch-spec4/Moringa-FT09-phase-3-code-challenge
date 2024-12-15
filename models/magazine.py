class Magazine:
    def __init__(self, mag_id, mag_name, mag_category):
        self._mag_id = mag_id
        self._mag_name = mag_name
        self._mag_category = mag_category

    @property
    def mag_id(self):
        return self._mag_id

    @property
    def mag_name(self):
        return self._mag_name

    @mag_name.setter
    def mag_name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._mag_name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def mag_category(self):
        return self._mag_category

    @mag_category.setter
    def mag_category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._mag_category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def create_magazine(self, cursor):
        # Inserting a new magazine
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", 
                       (self._mag_name, self._mag_category))
        self._mag_id = cursor.lastrowid
        return cursor

    @classmethod
    def get_all_magazines(cls, cursor):
        cursor.execute("SELECT * FROM magazines")
        all_magazines = cursor.fetchall()
        return [cls(magazine_data[0], magazine_data[1], magazine_data[2]) for magazine_data in all_magazines]

    def get_articles(self, cursor):
        # Fetching all articles associated with a magazine
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._mag_id,))
        articles_data = cursor.fetchall()
        return articles_data

    def get_contributors(self, cursor):
        # Fetching all authors who have contributed to a magazine
        cursor.execute("""
            SELECT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._mag_id,))
        contributors_data = cursor.fetchall()
        return contributors_data

    def get_article_titles(self, cursor):
        # Fetching article titles associated with a magazine
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._mag_id,))
        titles = [row[0] for row in cursor.fetchall()]
        return titles if titles else None

    def get_top_contributors(self, cursor):
        # Fetching authors who have contributed more than two articles to the magazine
        cursor.execute("""
            SELECT authors.*, COUNT(*) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._mag_id,))
        top_contributors = cursor.fetchall()
        return top_contributors if top_contributors else None
