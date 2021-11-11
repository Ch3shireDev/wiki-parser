from .service_interface import ServiceInterface


class ArticlesService(ServiceInterface):

    def __init__(self,
                 articles_downloader,
                 articles_storage):
        self.articles_downloader = articles_downloader
        self.articles_storage = articles_storage

    def download_next(self, count=1):
        urls = self.articles_storage.get_download_list(count)
        for url in urls:
            print(f"Downloading {url}")
            article_data = self.articles_downloader.download(url)
            self.articles_storage.add(article_data)

        return len(urls) > 0
