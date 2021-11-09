from storage_interface import StorageInterface
import pyodbc


class StorageArticlesDatabase(StorageInterface):
    def __init__(self):
        connect = pyodbc.connect(r'Driver={SQL Server};'
                                 r'Server=localhost\SQLEXPRESS;'
                                 r'Database=WIKI_DB;'
                                 r'Trusted_Connection=yes;',
                                 autocommit=True)

        connect.setencoding(encoding='utf-8')
        self.cursor = connect.cursor()
        self.element_to_download = None

    def are_elements_to_download(self):
        if self.element_to_download != None:
            return True
        else:
            self.element_to_download = self.next_element_to_download()
            return self.element_to_download != None

    def next_element_to_download(self):
        if self.element_to_download == None:
            self.cursor.execute("EXEC GET_ARTICLE_TO_DOWNLOAD")
            self.element_to_download = self.cursor.fetchval()

        element, self.element_to_download = self.element_to_download, None
        return element

    def add_element(self, article):
        params = (article["url"], article["title"], article["content"], str(article["info"]))
        self.cursor.execute(
            "EXEC INSERT_ARTICLE @ARTICLE_URL = ?, @ARTICLE_TITLE = ?, @ARTICLE_CONTENT = ?, @ARTICLE_INFO = ?", params)

    def add_elements_to_download(self, articles):
        for article in articles:
            self.cursor.execute(
                "EXEC INSERT_ARTICLE_TO_DOWNLOAD @ARTICLE_URL = ?", (article,))
