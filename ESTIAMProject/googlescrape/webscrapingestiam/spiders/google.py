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
        f = open("..\\user-agent", "r")
        for x in f:
            userAgents.append(x)
        
        f = open("..\\keyword.txt", "r")
        for x in f:
            KW.append(x)


        userA = userAgents[random.randint(1, 78)]
        yield scrapy.Request(url='https://google.com/search?q=Charlie+hebdo+et+racisme', callback=self.parse, headers={
            'User-Agent': userA
        }, meta={
            'userAgents' : userAgents,
            'keywords' : KW,
            'keywordIndex' : keywordIndex,
            'page': page
        }, dont_filter=True)

    def parse(self, response):
        print('ch7al?')
        userAgents = response.request.meta['userAgents']
        userA = userAgents[random.randint(1, 77)]
        KW = response.request.meta['keywords']
        keywordIndex = response.request.meta['keywordIndex']
        page = response.request.meta['page']

        liens = response.xpath("//div[@class='hlcw0c']/div/div/div/a")
        #print(liens)
        for lien in liens: #~10
            print('lien')
            titre = lien.xpath(".//h3/text()").get()
            lien2 = lien.xpath(".//@href").get()
            title, lienn, author, summary, keywords = self.newss(lien2)
            yield{
                'titre'     : title,
                'url'       : lienn,
                'auteur'    : author,
                'resume'    : summary,
                'mot clefs' : keywords
            }
            
        
        page = page + 10
        print(f'keywooord {keywordIndex}')
        if keywordIndex < 9:
            if page < 30:
                print("oui ou pas?")
                scrapingURL = f'https://google.com/search?q={KW[keywordIndex]}&start={page}'
                print(scrapingURL)
                yield scrapy.Request(url=scrapingURL, callback=self.parse, headers={
                    'User-Agent': userA
                }, meta={
                    'userAgents' : userAgents,
                    'keywords' : KW,
                    'keywordIndex' : keywordIndex,
                    'page': page
                }, dont_filter=True)
                #time.sleep(60)
            if page == 20:
                print("on quitte la")
                keywordIndex = keywordIndex + 1
                page = 0
                scrapingURL = f'https://google.com/search?q={KW[keywordIndex]}&start={page}'
                yield scrapy.Request(url=scrapingURL, callback=self.parse, headers={
                    'User-Agent': userA
                }, meta={
                    'userAgents' : userAgents,
                    'keywords' : KW,
                    'keywordIndex' : keywordIndex,
                    'page': page
                }, dont_filter=True)
                #time.sleep(60)
        
    def newss(self, lienn):
        print(f"le lien est : {lienn}")
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        article = Article(lienn, language="fr", config=config)
        article.download()
        article.parse()
        title = article.title
        author = article.authors
        print(f"l'auteur est : {author}")
        print(f"le titre est : {title}")
        article.nlp()
        summary = article.summary
        keywords = article.keywords

        return title, lienn, author, summary, keywords;        