import scrapy


class GBChealthSpider(scrapy.Spider):
    name = 'gbchealth'

    start_urls = ['http://www.gbchealth.org/news/']

    def parse(self, response):

        for article in response.css('.entry-wrap'):
            article_url = article.css('h2.entry-title a::attr(href)').extract_first()
            yield scrapy.Request(article_url, callback=self.parse_article)
        
        next_page = response.css('.pagination.pagination-centered ul li a::attr(href)').getall()[-1]
        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

        else:
            print()
            print('No Page Left')
            print()

    
    def parse_article(self, response):
        title = response.css('.entry-title::text').get()
        date = response.css('.entry-date::text').get()
        posts = response.css('.entry-content.content')

        all_text = ""
        
        for post in posts.xpath('.//p//text()').extract():
            text = post
            all_text = all_text + text

        yield {
            'Title': title,
            'post': all_text,
            'date': date 
        }
