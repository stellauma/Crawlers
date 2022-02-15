import scrapy
import PyPDF2
from scrapy_splash import SplashRequest
from ..items import BlogItem

class mednewsSpider(scrapy.Spider):
    name = 'mednews'

    # start_urls = [
    #     "https://www.medicalnewstoday.com/search?q=NIGERIA",
    #     ]
    domain = 'medicalnewstoday.com'
    allowed_domains = ['medicalnewstoday.com','www.medicalnewstoday.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
    def start_requests(self):
        yield SplashRequest(url="https://www.medicalnewstoday.com/search?q=NIGERIA", callback=self.parse, args={"wait": 3,'html': 1, 'iframes': 1})

    def parse(self, response):
        print('*************')
        # print(response.css('.gsc-webResult.gsc-result'))
        for posts in response.css('.gsc-webResult.gsc-result'):
            link =  posts.css('a.gs-title::attr(href)').get()
            print(link)
            yield SplashRequest(link, callback=self.parseBlog)

        # next_page = response.css('.gsc-cursor .gsc-cursor-page').get()
        # # print(next_page)
        # iframe_html = response.data['childFrames'][0]['html']
        # print(iframe_html)
        # if next_page is not None:
        #     yield SplashRequest(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['domain'] = self.domain
        blog['title']= response.css('div.css-z468a2 h1::text').get() 
        blog['author'] = response.css('section.css-19y29pm span a.css-1g08k51::text').getall()[-1]
        blog['published']= response.css('section.css-19y29pm div span::text').getall()[-1]
        # blog['content'] = " ".join(response.css('article p::text').getall())
        blog['url']= response.url
        yield blog
