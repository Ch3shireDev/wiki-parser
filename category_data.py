import bs4
import requests


class CategoryData:

    def __init__(self, base_url, route):
        self.base_url = base_url
        self.url = route
        data = requests.get(self.base_url + route).text
        self.bs = bs4.BeautifulSoup(data, "html.parser")
        self.links = list(self.get_links_internal())

    def get_dict(self):
        return {
            'url': self.url,
            'title': self.get_title(),
            'content': self.get_content().strip(),
            'articles': list(self.get_articles()),
            'categories': list(self.get_categories())
        }

    def get_categories(self):
        for link in self.links:
            if not link['url'].startswith('/wiki/Category:'):
                continue
            yield link['url']

    def get_articles(self):
        for link in self.links:
            if link['url'].startswith('/wiki/Category:'):
                continue
            yield link['url']

    def get_title(self):
        return self.bs.find("h1", {"id": "firstHeading"}).text

    def get_content_list(self):
        container = self.bs.select("div.mw-parser-output > *")
        description = []
        for element in container:
            if self.can_skip_content(element):
                continue
            description += [*self.get_unordered_list(element)]
            description += [*self.get_ordered_list(element)]
            description += [*self.get_paragraphs(element)]
        return description

    def get_content(self):
        content_list = self.get_content_list()
        return str.join("\n", content_list).strip()

    def can_skip_content(self, element):
        return element.name == "table"

    def get_unordered_list(self, element):
        if element.name == "ul":
            for element_ul in element.select("li"):
                yield f"- {element_ul.text}"
            yield ""

    def get_ordered_list(self, element):
        if element.name == "ol":
            i = 1
            for element_ol in element.select("li"):
                yield f"{i}. {element_ol.text}"
                i += 1
            yield ""

    def get_paragraphs(self, element):
        if element.name == "p":
            yield f"{element.text}"

    def get_links_internal(self):
        links = []

        for sub_category in self.bs.find_all("div", class_="mw-category"):
            for link in sub_category.find_all("a"):
                url = link.get("href")
                title = link.text
                links.append({"url": url, "title": title})

        next_page_link = self.find_next_page_link()
        if next_page_link == None:
            return links

        print(next_page_link)
        links += list(self.get_links_from_next_page(next_page_link))
        return links

    def find_next_page_link(self):
        for link in self.bs.find_all("a"):
            if link.text == "next page":
                return link.get("href")

    def get_links_from_next_page(self, next_page_link):
        bs = CategoryData(self.base_url, next_page_link)
        return bs.get_links_internal()
