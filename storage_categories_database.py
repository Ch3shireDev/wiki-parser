from storage_interface import StorageInterface
import pyodbc


class StorageCategoriesDatabase(StorageInterface):
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
            self.cursor.execute("EXEC GET_CATEGORY_TO_DOWNLOAD")
            self.element_to_download = self.cursor.fetchval()

        category, self.element_to_download = self.element_to_download, None
        return category

    def add_element(self, category):
        params = (category["url"], category["title"], category["content"])
        self.cursor.execute(
            "EXEC INSERT_CATEGORY @CATEGORY_URL = ?, @CATEGORY_TITLE = ?, @CATEGORY_CONTENT = ?", params)

    def add_elements_to_download(self, categories):
        for category in categories:
            self.cursor.execute(
                "EXEC INSERT_CATEGORY_TO_DOWNLOAD @CATEGORY_URL = ?", (category,))

