import scrapy
from ..items import BlogItem

class healthdataSpider(scrapy.Spider):
    name = 'healthd'

    start_urls = [
        "http://www.healthdata.org/news-events/news-releases",
        ]
    domain = 'healthdata.org'
    allowed_domains = ['healthdata.org', 'www.healthdata.org']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    def parse(self, response):
        for posts in response.css('.view-content > div'):
            link =  posts.css('.views-field.views-field-title .field-content a::attr(href)').get()
            yield response.follow(link, callback=self.parseBlog)

        next_page = response.css('.pager-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['domain'] = self.domain
        # blog['author'] = response.css('.c-article-author-list__item > a::text').getall()
        blog['title']= response.css('.page__title.title::text').get()
        blog['published']= response.css('.date-display-single::text ').get()
        blog['content'] = " ".join(lines.strip() for lines in response.css('.field-item.even p::text').getall())
        blog['url']= response.url
        yield blog
