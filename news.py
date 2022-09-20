from platform import architecture
from newsapi import NewsApiClient

class news():
    def __init__(self):
        self.newsapi = NewsApiClient(
            api_key='83e632d7a4ed436ea3225f8aa997136a')
        # /v2/top-headlines
        self.country = None
        self.domains = None
        self.excludeDomains = None
        self.fromDate = None
        self.toDate = None
        self.language = 'en'
        self.q = None
        self.category = None
        
    def getTopArticles(self):
        self.top_headlines = self.newsapi.get_top_headlines()
        for i in self.top_headlines['articles']:
             print('PUBLSIHED:', i['publishedAt'],
                       i['source']['name'], i['title'], i['url'], '\n')
            

