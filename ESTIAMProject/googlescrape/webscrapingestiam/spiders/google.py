import scrapy
from newspaper import Article
from newspaper import Config
import random
import time


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['www.google.com']
    start_urls = ['https://google.com/search?q=test']

    googleLink = 'https://www.google.com/search?q=test&oq=test&aqs=chrome.0.69i59l2j0j69i65l2j69i61l3.492j0j7&sourceid=chrome&ie=UTF-8'

    def start_requests(self):
        userAgents = []
        KW = []
        page = 0
        keywordIndex = 0
        f = open("..\\user-agent.txt", "r")
        for x in f:
            userAgents.append(x)

        f = open("..\\keyword.txt", "r")
        for x in f:
            KW.append(x)

        userA = userAgents[random.randint(1, 78)]
        yield scrapy.Request(url='https://google.com/search?q=Charlie+hebdo+et+racisme', callback=self.parse, headers={
            'User-Agent': userA
        }, meta={
            'userAgents': userAgents,
            'keywords': KW,
            'keywordIndex': keywordIndex,
            'page': page
        }, dont_filter=True)

    def parse(self, response):
        userAgents = response.request.meta['userAgents']
        userA = userAgents[random.randint(1, 77)]
        KW = response.request.meta['keywords']
        keywordIndex = response.request.meta['keywordIndex']
        page = response.request.meta['page']

        liens = response.xpath("//div[@class='hlcw0c']/div/div/div/div/a")
        for lien in liens:  # ~10
            titre = lien.xpath(".//h3/text()").get()
            lien2 = lien.xpath(".//@href").get()
            title, lienn, author, summary, keywords = self.newss(lien2)
            yield{
                'titre': title,
                'url': lienn,
                'auteur': author,
                'resume': summary,
                'mot clefs': keywords
            }

        page = page + 10
        if keywordIndex < 6:
            if page < 20:
                scrapingURL = f'https://google.com/search?q={KW[keywordIndex]}&start={page}'
                yield scrapy.Request(url=scrapingURL, callback=self.parse, headers={
                    'User-Agent': userA
                }, meta={
                    'userAgents': userAgents,
                    'keywords': KW,
                    'keywordIndex': keywordIndex,
                    'page': page
                }, dont_filter=True)
            if page == 20:
                keywordIndex = keywordIndex + 1
                page = 0
                scrapingURL = f'https://google.com/search?q={KW[keywordIndex]}&start={page}'
                yield scrapy.Request(url=scrapingURL, callback=self.parse, headers={
                    'User-Agent': userA
                }, meta={
                    'userAgents': userAgents,
                    'keywords': KW,
                    'keywordIndex': keywordIndex,
                    'page': page
                }, dont_filter=True)

    def newss(self, lienn):
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        article = Article(lienn, language="fr", config=config)
        article.download()
        article.parse()
        title = article.title
        author = article.authors
        article.nlp()
        summary = article.summary
        keywords = article.keywords

        return title, lienn, author, summary, keywords
