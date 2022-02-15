import scrapy
from ..items import BlogItem

class biomedSpider(scrapy.Spider):
    name = 'biomed'

    start_urls = [
        "https://www.biomedcentral.com/search?query=nigeria+&searchType=publisherSearch",
        ]
    domain = 'biomedcentral.com'
    allowed_domains = ['biomedcentral.com', 'www.biomedcentral.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    def parse(self, response):
        for posts in response.css('.c-list-group.c-list-group--bordered.c-list-group.c-list-group--md .c-list-group__item'):
            link =  posts.css('h3.c-listing__title a::attr(href)').get()
            yield response.follow(link, callback=self.parseBlog)

        next_page = response.css('.c-pagination__item a::attr(href)').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['domain'] = self.domain
        blog['author'] = response.css('.c-article-author-list__item > a::text').getall()
        blog['title']= response.css('.c-article-title::text').get()
        blog['published']= response.css('.c-article-identifiers__item > a >time::text ').get()
        blog['content'] = " ".join(response.css('.col-lg-8.single-page-content p::text').getall())
        blog['url']= response.url
        yield blog
