import scrapy
from ..items import BlogItem

class HealthSpider(scrapy.Spider):
    name = 'xspiderH'

    start_urls = [
        "http://www.healthnews.ng/?s=",
        ]
    domain = 'www.healthnews.ng'
    allowed_domains = ['www.healthnews.ng']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

    def parse(self, response):
        for posts in response.xpath('article.jeg_post.jeg_pl_md_2.format-standard'):
            link =  posts.css('h3.jeg_post_title a::attr(href)').get()
            yield response.follow(link, callback=self.parseBlog)

        next_page = response.css('a.page_nav.next::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseBlog(self, response):
        blog = BlogItem()
        blog['title']= response.css('.jeg_post_title span::text').get()
        blog['domain'] = self.domain
        blog['published']= response.css('.jeg_meta_date a::text').get()
        blog['author'] = response.css('.jeg_meta_author.coauthor a::text').get()
        blog['url']= response.url
        blog['content'] =  " ".join(response.css('.entry-content.with-share p::text').getall())

        yield blog

