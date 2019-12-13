# -*- coding: utf-8 -*-
import scrapy
from ..items import HomedepotItem


class HomedepotSpider(scrapy.Spider):
    name = 'homedepot'

    #how many pages you want to scrape
    no_of_pages= 6
    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}
    allowed_domains = ['homedepot.com']
    start_urls = ['http://www.homedepot.com/']

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.homedepot.com/s/heat%2520gun?NCNI-5"]

        #% page for page in range(1,6)
               #['http://example.com/foo/bar/page_%s' % page for page in range(1,54)]

        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

 

    def parse(self, response):
        
        
        self.no_of_pages -= 1
        #print(response.text)

        hamilton_res =response.xpath(".//div[@data-podaction='product name']/a/@href").getall()
        
        
        # print(len(greentop_res))

        for ham in hamilton_res:
            final_url = response.urljoin(ham)
            yield scrapy.Request(url=final_url, callback = self.parse_greentop, headers = self.headers)
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
    
            
    def parse_greentop(self, response):
        
        Category='NA'
        Sub_category=response.xpath(".//div[@class='pdf data-link']/@data-link").get() or 'NA'
        Product_Name = response.xpath(".//h1[@class='product-title__title']//text()").get()
        Product_ID =response.xpath(".//span[@id='product_store_sku']//text()").get()or "NA"
        Product_Model =(response.xpath(".//h2[@class='product_details modelNo']//text()").get()).split()[2] or "NA"
        Product_Brand = response.xpath(".//div[@class='sticky_brand_info']//text()").get() or "NA"
        

        Price =  '$'+(response.xpath(".//span[@itemprop='price']/@content").get())
        print(Price)
        #if len(Price) > 1: Price = Price[1].get()
        #elif len(Price) == 1: Price = Price[0].get()
        #else : Price = Price.get()

        Features= response.xpath("(.//ul[@class='list']/li//text())").get() or "NA"
        #instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        #instock = instock.strip() == "In stock."
        #reviews = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath(".//p[@itemdrop='description']").get() or "NA"

        Img_url = response.xpath(".//img[@id='mainImage']/@src").get()
        Website="Homedepot"

        #Description = []
        #for description_temp in description_raw:
            
            #Description.append(description_temp.strip())

        print(Category,Sub_category,Product_Name,Product_ID,Product_Model,Product_Brand,Img_url)
        # print(final_review)
        # print(reviews)
        # print(description)

        yield HomedepotItem(Category=Category,Website=Website,Sub_category=Sub_category,Product_Name = Product_Name,Product_ID = Product_ID,Product_Model =Product_Model,Product_Brand = Product_Brand,Price = Price, Features = Features, Description = description_raw, Image_urls = [Img_url])



            
        
