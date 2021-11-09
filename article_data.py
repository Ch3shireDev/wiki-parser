import requests
from bs4 import BeautifulSoup
import re


class ArticleData:

    def __init__(self, base_url, page_route):
        data = requests.get(base_url + page_route)
        self.bs = BeautifulSoup(data.text, 'html.parser')
        self.content = self.bs.find('div', {'id': 'content'})

    def get_dict(self):
        return {
            'info': self.get_info(),
            'categories': list(self.get_categories()),
            'keywords': list(self.get_keywords())
        }

    def get_info(self):
        infobox = self.content.find('table', {'class': 'infobox'})

        info_dict = {}

        for row in infobox.find_all('tr'):

            label_element = row.find('th', {'class': 'infobox-label'})
            label_data = row.find('td', {'class': 'infobox-data'})

            if not label_element or not label_data:
                continue

            label = label_element.text
            value = label_data.text.replace('\xa0', ' ')
            value = re.sub('\s+', ' ', value)
            value = re.sub('\[\d+\]', '', value)

            info_dict[label] = value

        return info_dict

    def get_categories(self):
        keywords = self.content.find('div', {'id': 'mw-normal-catlinks'})
        keywords = keywords.find_all('a')
        links = [LinkData(keyword) for keyword in keywords]
        return [link for link in links if link.is_valid]

    def get_keywords(self):
        paragraphs = self.content.find_all('p')
        for paragraph in paragraphs:
            keywords = paragraph.find_all('a')
            for keyword in keywords:
                link = LinkData(keyword)
                if link.is_valid:
                    yield link

    def get_first_paragraph(self):
        paragraphs = self.content.find_all('p')
        if len(paragraphs) > 0:
            return paragraphs[0].text
        else:
            return ''


class LinkData:

    def __init__(self, link_element):
        self.is_valid = 'title' in link_element.attrs
        if not self.is_valid:
            return
        self.text = link_element.text
        self.link = link_element.attrs['href']
        self.title = link_element.attrs['title']

    def __repr__(self):
        return f'{self.text} ({self.link})'


if __name__ == '__main__':
    base_url = 'https://en.wikipedia.org'
    page_url = '/wiki/Blender_(software)'

    page = ArticleData(base_url, page_url).get_dict()
    print(page)
