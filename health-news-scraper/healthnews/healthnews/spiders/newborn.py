import scrapy
from ..items import BlogItem

class biomedSpider(scrapy.Spider):
    name = 'newbnet'

    start_urls = [
        "https://www.healthynewbornnetwork.org/blog/",
        ]
    domain = 'healthynewbornnetwork.org'
    allowed_domains = ['healthynewbornnetwork.org', 'www.healthynewbornnetwork.org']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    def parse(self, response):
        for posts in response.css('article.article'):
            link =  posts.css('a::attr(href)').get()
            yield response.follow(link, callback=self.parseBlog)

        next_page = response.css('.next.page-numbers::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['domain'] = self.domain
        if response.css('section.col-lg-3.sidebar-details > p:nth-child(4) a::text').getall():
            blog['author'] = response.css('section.col-lg-3.sidebar-details > p:nth-child(4) a::text').getall()
        else:
            blog['author'] = response.css('section.col-lg-3.sidebar-details > p:nth-child(4)::text').getall()
        blog['title']= response.css('.entry-title::text').get()
        blog['published']= response.css('time.updated::text ').get()
        blog['content'] = " ".join(response.css('.entry-content p::text').getall())
        blog['url']= response.url
        yield blog