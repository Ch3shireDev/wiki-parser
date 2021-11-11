from .storage_interface import StorageInterface
import pyodbc


class ArticlesDatabase(StorageInterface):
    def __init__(self):
        connect = pyodbc.connect(r'Driver={SQL Server};'
                                 r'Server=localhost\SQLEXPRESS;'
                                 r'Database=WIKI_DB;'
                                 r'Trusted_Connection=yes;',
                                 autocommit=True)
        connect.setencoding(encoding='utf-16le')
        self.cursor = connect.cursor()

    def get_download_list(self, count: int) -> list:
        self.cursor.execute("EXEC GET_ARTICLES_TO_DOWNLOAD @COUNT=?", (count,))
        urls = [url for (url,) in self.cursor.fetchall()]
        return urls

    def add(self, article: dict):
        params = (article["url"], article["title"],
                  article["content"], str(article["info"]))
        self.cursor.execute(
            "EXEC ADD_ARTICLE @ARTICLE_URL = ?, @ARTICLE_TITLE = ?, @ARTICLE_CONTENT = ?, @ARTICLE_INFO = ?", params)
        for keyword in article["keywords"]:
            params = (keyword['url'], article['url'],
                      keyword['title'], keyword['text'])
            self.cursor.execute(
                "EXEC ADD_KEYWORD @KEYWORD_URL=?, @ARTICLE_URL=?, @KEYWORD_TITLE=?, @KEYWORD_TEXT=?", params)

        for category in article["categories"]:
            params = (article['url'], category['url'])
            self.cursor.execute(
                "EXEC ADD_ARTICLE_CATEGORY_RELATION @ARTICLE_URL = ?, @CATEGORY_URL = ?", params)

    def add_to_download(self, article: list):
        params = (article['url'],)
        self.cursor.execute(
            "EXEC ADD_ARTICLE_TO_DOWNLOAD @ARTICLE_URL = ?", params)
