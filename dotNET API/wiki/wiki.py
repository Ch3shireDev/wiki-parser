
from lib import BsService
import yaml

base_url = "https://en.wikipedia.org"

links = []
categories_to_search = ['/wiki/Category:Software']

found_categories = []

found_categories_set = set()

found_links = []

while len(categories_to_search) > 0:

    category_url = categories_to_search.pop()

    if category_url in found_categories_set:
        continue

    found_categories_set.add(category_url)

    bs = BsService(base_url, category_url)
    title = bs.get_title()
    content = bs.get_content()

    links = []

    for link in bs.get_links():
        if link['url'].startswith('/wiki/Category:'):
            categories_to_search.append(link['url'])
        else:
            links.append(link)

    category = {
        'title': title,
        'content': content,
        'links': links
    }

    found_links += links

    found_categories.append(category)

    print(title)
    print(len(found_links))

    with open('wiki.yml', 'w') as f:
        yaml.dump(found_categories, f)
        f.close()
