from storage_interface import StorageInterface


class StorageMemory(StorageInterface):

    def __init__(self):
        self.categories_to_download = []
        self.categories = []

    def are_categories_to_download(self):
        return len(self.categories_to_download) > 0

    def get_next_category_to_download(self):
        return self.categories_to_download.pop()

    def add_categories_to_download(self, categories):
        self.categories_to_download += categories

    def add_category_data(self, category):
        self.categories.append(category)

    def add_articles_to_download(self, articles):
        pass

    def add_article_data(self, article):
        pass
