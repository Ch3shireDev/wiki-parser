from storages import *
from services import *
from downloaders import *

base_url = "https://en.wikipedia.org"
articles_prefix = '/wiki/'
categories_prefix = '/wiki/Category:'

links = []

categories_storage: StorageInterface = CategoriesDatabase()
articles_storage: StorageInterface = ArticlesDatabase()

categories_downloader: DownloaderInterface = CategoriesDownloader(base_url, categories_prefix)
articles_downloader: DownloaderInterface = ArticlesDownloader(base_url, articles_prefix)

categories_service: ServiceInterface = CategoriesService(
    categories_downloader, categories_storage, articles_storage)
# articles_service: ServiceInterface = ArticlesService(
#     articles_downloader, articles_storage)

categories_storage.add_to_download({'url': 'Software'})

while True:
    category_result = categories_service.download_next()
    # article_result = articles_service.download_next()

