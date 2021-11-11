from .service_interface import ServiceInterface


class CategoriesService(ServiceInterface):

    def __init__(self,
                 categories_downloader,
                 categories_storage,
                 articles_storage):
        self.categories_storage = categories_storage
        self.categories_downloader = categories_downloader
        self.articles_storage = articles_storage

    def download_next(self, count=1):
        urls = self.categories_storage.get_download_list(count)
        for url in urls:
            print(f"Downloading {url}")
            category_data = self.categories_downloader.download(url)
            
            print(category_data["title"])
            for category in category_data["categories"]:
                print(category['title'])
            for article in category_data["articles"]:
                print(article['title'])
            answer = input("Kontynuować? [y/n]: ")
            if answer != "y":
                self.categories_storage.remove(category_data)
                continue
            
            self.categories_storage.add(category_data)
            
            for article in category_data['articles']:
                print(f"Adding {article['url']} to download")
                self.articles_storage.add_to_download(article)

        return len(urls) > 0