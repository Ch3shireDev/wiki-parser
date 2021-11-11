import bs4
import requests


class BsService:

    def __init__(self, base_url, route):
        self.base_url = base_url
        self.route = route
        self.bs = PageService(base_url).get_bs(route)

    def get_title(self):
        """
        Get the title of the page.
        """
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
        """
        Check if the element can be skipped.
        """
        if element.name == "table":
            return True
        return False

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

    def get_links(self):
        for sub_category in self.bs.find_all("div", class_="mw-category"):
            for link in sub_category.find_all("a"):
                url = link.get("href")
                title = link.text
                yield {"url": url, "title": title}

        next_page_link = self.find_next_page_link()
        if next_page_link:
            for link in self.get_links_from_next_page(next_page_link):
                yield link

    def find_next_page_link(self):
        for link in self.bs.find_all("a"):
            if link.text == "next page":
                return link.get("href")

    def get_links_from_next_page(self, next_page_link):
        bs = BsService(self.base_url, next_page_link)
        for link in bs.get_links():
            yield link


class PageService:

    def __init__(self, base_url):
        self.base_url = base_url

    def get_page(self, route):
        """
        Get the page from the url.
        """
        response = requests.get(self.base_url + route)
        return response.text

    def get_bs(self, route):
        data = self.get_page(route)
        return bs4.BeautifulSoup(data, "html.parser")
