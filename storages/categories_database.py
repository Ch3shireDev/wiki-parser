from .storage_interface import StorageInterface
import pyodbc


class CategoriesDatabase(StorageInterface):
    def __init__(self):
        connect = pyodbc.connect(r'Driver={SQL Server};'
                                 r'Server=localhost\SQLEXPRESS;'
                                 r'Database=WIKI_DB;'
                                 r'Trusted_Connection=yes;',
                                 autocommit=True)

        connect.setencoding(encoding='utf-16le')
        self.cursor = connect.cursor()
        self.elements_to_download = None

    def get_download_list(self, count: int) -> list:
        self.cursor.execute(
            "EXEC GET_CATEGORIES_TO_DOWNLOAD @COUNT=?", (count,))
        self.elements_to_download = [url for (url,) in self.cursor.fetchall()]
        return self.elements_to_download

    def add(self, category: dict):
        params = (category["url"], category["title"], category["content"])
        self.cursor.execute(
            "EXEC ADD_CATEGORY @CATEGORY_URL = ?, @CATEGORY_TITLE = ?, @CATEGORY_CONTENT = ?", params)

        for subcategory in category["categories"]:
            self.cursor.execute(
                'EXEC ADD_CATEGORY_TO_DOWNLOAD @CATEGORY_URL = ?', (subcategory["url"],))
            self.cursor.execute(
                'EXEC ADD_CATEGORY_RELATION @CATEGORY_PARENT_URL = ?, @CATEGORY_CHILD_URL = ?', (category["url"], subcategory["url"]))

        for article in category["articles"]:
            params = (article["url"], category["url"])
            self.cursor.execute(
                'EXEC ADD_ARTICLE_CATEGORY_RELATION @ARTICLE_URL = ?, @CATEGORY_URL = ?', params)

    def add_to_download(self, category: dict):
        category_url = category["url"]
        self.cursor.execute(
            "EXEC ADD_CATEGORY_TO_DOWNLOAD @CATEGORY_URL = ?", (category_url,))

    def remove(self, category: dict):
        self.cursor.execute(
            "EXEC DELETE_CATEGORY @CATEGORY_URL = ?", (category["url"],))
