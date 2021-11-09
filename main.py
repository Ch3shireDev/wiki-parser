from article_data import ArticleData

base_url = 'https://en.wikipedia.org'
page_url = '/wiki/Blender_(software)'

page = ArticleData(base_url, page_url).get_dict()
