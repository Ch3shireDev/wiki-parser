import requests
from bs4 import BeautifulSoup
import re


class ArticleData:

    def __init__(self, base_url, prefix, page_route):
        self.url = page_route
        self.prefix = prefix
        data = requests.get(base_url + prefix + page_route)
        self.bs = BeautifulSoup(data.text, 'html.parser')
        self.content = self.bs.find('div', {'id': 'content'})

    def get_dict(self):
        return {
            'url': self.url.replace('/wiki/', ''),
            'title': self.get_title().strip(),
            'content': self.get_first_paragraph().strip(),
            'info': self.get_info(),
            'categories': list(self.get_categories()),
            'keywords': list(self.get_keywords()),
            'is_valid': self.url.startswith('/wiki/')
        }

    def get_title(self):
        return self.bs.find('h1').text

    def get_info(self):
        infobox = self.content.find('table', {'class': 'infobox'})

        if infobox is None:
            return {}

        info_dict = {}

        for row in infobox.find_all('tr'):

            label_element = row.find('th', {'class': 'infobox-label'})
            label_data = row.find('td', {'class': 'infobox-data'})

            if not label_element or not label_data:
                continue

            label = label_element.text
            value = label_data.text.replace('\xa0', ' ')
            value = label_data.text.replace('\n', ', ')
            value = re.sub('\[\d+\]', ' ', value)
            value = re.sub('\s+', ' ', value)

            info_dict[label] = value

        return info_dict

    def get_categories(self):
        keywords = self.content.find('div', {'id': 'mw-normal-catlinks'})
        keywords = keywords.find_all('a')
        links = [KeywordData(keyword, self.url).get_dict()
                 for keyword in keywords]
        return [link for link in links if link['is_valid']]

    def get_keywords(self):
        paragraphs = self.content.find_all('p')
        for paragraph in paragraphs:
            keywords = paragraph.find_all('a')
            for keyword in keywords:
                link_data = KeywordData(keyword, self.url)
                if link_data.is_valid:
                    yield link_data.get_dict()

    def get_first_paragraph(self):
        paragraphs = self.content.find_all('p')
        for paragraph in paragraphs:
            if paragraph.text and paragraph.text.strip():
                p = paragraph.text.strip()
                p = re.sub('\[\d+\]', '', p)
                return p
        return ''


class KeywordData:

    def __init__(self, link_element, article_url):
        self.article_url = article_url
        self.is_valid = 'title' in link_element.attrs
        if not self.is_valid:
            return
        self.text = link_element.text
        self.url = link_element.attrs['href']
        self.title = link_element.attrs['title']
        if not self.url.startswith('/wiki/'):
            self.is_valid = self.url.startswith('/wiki/')

        if '(page does not exist)' in self.title:
            self.is_valid = False

    def __repr__(self):
        return f'{self.text} ({self.url})'

    def get_dict(self):

        return {
            'url': self.url.replace('/wiki/', '').replace('Category:', ''),
            'title': self.title,
            'text': self.text,
            'is_valid': self.is_valid
        }
