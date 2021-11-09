from article_data import ArticleData
from category_data import CategoryData
from storage_categories_database import StorageCategoriesDatabase
from storage_articles_database import StorageArticlesDatabase
from storage_memory import StorageMemory
import yaml


base_url = "https://en.wikipedia.org"

links = []

categories = StorageCategoriesDatabase()
categories.add_elements_to_download(['/wiki/Category:Software'])

articles = StorageArticlesDatabase()

while categories.are_elements_to_download() or categories.are_articles_to_download():

    if category_url := categories.next_element_to_download():
        print(category_url)
        category = CategoryData(base_url, category_url).get_dict()
        categories.add_element(category)
        categories.add_elements_to_download(category['categories'])
        articles.add_elements_to_download(category['articles'])

        print(category['title'])

    if article_url := articles.next_element_to_download():
        article = ArticleData(base_url, article_url).get_dict()
        articles.add_element(article)

        print(article['title'])
