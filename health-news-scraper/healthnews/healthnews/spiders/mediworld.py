import scrapy
from ..items import BlogItem

class mediSpider(scrapy.Spider):
    name = 'medworld'

    start_urls = [
        "https://medicalworldnigeria.com/news/medical-news?page=1",
        ]
    domain = 'medicalworldnigeria.com'
    allowed_domains = ['medicalworldnigeria.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    def parse(self, response):
        for posts in response.css('.newz.md-20'):
            link =  posts.css('div.content h5 a::attr(href)').get()
            yield response.follow(link, callback=self.parseBlog)

        next_page = response.css('div.pagination ul a::attr(href)').getall()[-1]
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['domain'] = self.domain
        blog['title']= response.css('div.row.section-seperator.latest-news.mt-40.md-40 .col-lg-8 h3::text').get()
        blog['published']= response.css('.col-lg-8.single-page-content small::text').get().split(':')[-1]
        blog['content'] = " ".join(response.css('.col-lg-8.single-page-content p::text').getall())
        blog['url']= response.url
        yield blog
