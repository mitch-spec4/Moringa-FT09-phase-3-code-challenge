class Article:
    def __init__(self, article_id, headline, body, writer_id, journal_id):
        self._article_id = article_id
        self.headline = headline
        self.body = body
        self._writer_id = writer_id
        self._journal_id = journal_id

    @property
    def article_id(self):
        return self._article_id

    @property
    def headline(self):
        return self._headline

    @headline.setter
    def headline(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 60:
            self._headline = value
        else:
            raise ValueError("Headline must be a string between 5 and 60 characters")

    @staticmethod
    def create_article(cursor, headline, body, writer_id, journal_id):
        cursor.execute("INSERT INTO articles (headline, body, writer_id, journal_id) VALUES (?, ?, ?, ?)", 
                       (headline, body, writer_id, journal_id))
        article_id = cursor.lastrowid
        return Article(article_id, headline, body, writer_id, journal_id)

    @staticmethod
    def get_all_titles(cursor):
        cursor.execute("SELECT headline FROM articles")
        titles = cursor.fetchall()
        return [title[0] for title in titles] if titles else []

    def get_writer_name(self, cursor):
        cursor.execute("SELECT name FROM writers WHERE id = ?", (self._writer_id,))
        writer_name = cursor.fetchone()
        return writer_name[0] if writer_name else None

    def get_journal_name(self, cursor):
        cursor.execute("SELECT name FROM journals WHERE id = ?", (self._journal_id,))
        journal_name = cursor.fetchone()
        return journal_name[0] if journal_name else None
