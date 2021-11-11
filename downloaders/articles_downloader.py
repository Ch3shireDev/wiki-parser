from .downloader_interface import DownloaderInterface
from .category_data import CategoryData
from .article_data import ArticleData


class ArticlesDownloader(DownloaderInterface):

    def __init__(self, base_url, prefix):
        self.base_url = base_url
        self.prefix = prefix

    def download(self, url):
        return ArticleData(self.base_url, self.prefix, url).get_dict()
