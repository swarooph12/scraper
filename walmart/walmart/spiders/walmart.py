# -*- coding: utf-8 -*-
import scrapy
from ..items import WalmartItem



class WalmartSpider(scrapy.Spider):
    name = 'walmart'

    #how many pages you want to scrape
    no_of_pages= 6
    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}
    allowed_domains = ['walmart.com']
    #start_urls = ['http://www.walmart.com/']
    def __init__(self, product=None,brand=None,*args,**kwargs):
        self.start_urls = [f'https://www.walmart.com/search/?query={product}+{brand}']  # py36
        super().__init__(*args,**kwargs)
        
    def start_requests(self):
        # starting urls for scraping
        urls = self.start_urls

        #% page for page in range(1,6)
               #['http://example.com/foo/bar/page_%s' % page for page in range(1,54)]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

 

    def parse(self, response):
        
        
        self.no_of_pages -= 1
        # print(response.text)

        walmart_res =response.xpath("//a[@class='product-title-link line-clamp line-clamp-2']/@href").getall()
        
        # print(len(greentop_res))

        for wal in walmart_res:
            final_url = response.urljoin(wal)
            yield scrapy.Request(url=final_url, callback = self.parse_walmart, headers = self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)
        if(self.no_of_pages > 0):
            
            next_page_url = response.xpath("//a[@class='pagination-link']").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)
            
    def parse_walmart(self, response):
        Category_Name="Crawling"
        Sub_category="Accessories"
        Product_Name = response.xpath(".//h1[@class='prod-ProductTitle font-normal']//text()").get()
        Product_ID =response.xpath(".//div[@class='valign-middle secondary-info-margin-right copy-mini display-inline-block wm-item-number']//text()").get()
        Product_Model =response.xpath(".//div[@class='valign-middle secondary-info-margin-right copy-mini display-inline-block other-info']//text()").get()
        Product_Brand = response.xpath(".//a[@class='prod-brandName']/span//text()").get() or "NA"
        

        Price =  response.xpath(".//span[@class='price-currency']//text()").get()+response.xpath("//span[@class='price-characteristic']//text()").get()+response.xpath("//span[@class='price-mark']//text()").get()+response.xpath("//span[@class='price-mantissa']//text()").get()
        print(Price)
        #if len(Price) > 1: Price = Price[1].get()
        #elif len(Price) == 1: Price = Price[0].get()
        #else : Price = Price.get()

        Features= response.xpath(".//div[@class='tab-content is-active']/ul").get() or "NA"
        #instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        #instock = instock.strip() == "In stock."
        #reviews = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath(".//div[@class='about-desc']//text()").get()or "NA"

        Img_url = 'https:'+(response.xpath(".//img[@class='prod-hero-image-carousel-image']/@src").get())

        #Description = []
        #for description_temp in description_raw:
            
            #Description.append(description_temp.strip())

        print(Category_Name,Sub_category,Product_Name,Product_ID,Product_Model,Product_Brand,Img_url)
        # print(final_review)
        # print(reviews)
        # print(description)

        yield WalmartItem(Category_Name=Category_Name,Sub_category=Sub_category,Product_Name = Product_Name,Product_ID = Product_ID,Product_Model =Product_Model,Product_Brand = Product_Brand,Price = Price, Features = Features, Description = description_raw, Image_urls = [Img_url])



            
        
