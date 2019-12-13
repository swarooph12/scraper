import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from flask import json
from urllib import parse
from flask import Flask
from flask_restful import Resource, Api, reqparse

from gevent.pywsgi import WSGIServer

app = Flask(__name__)
api = Api(app)


class SteamSearch(Resource):
    def put(self):
        
        
        parser = reqparse.RequestParser()
        parser.add_argument('query', required=True,
                            help='A search term needs to be provided')
        parser.add_argument('brand', required=True,
                            help='A search term needs to be provided')                    
        
        args = parser.parse_args()

        product = parse.urlencode({'query': args.query})
        brand=(parse.urlencode({'brand':args.brand})).split("=")[1]
        find=product+'+'+brand
        print(find)
        
s=get_project_settings()
process = CrawlerProcess(s)
process.crawl('ebay',find)
       
process.start()


print ('Crawling Completed')        

api.add_resource(SteamSearch, '/query')

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=5000,debug=True)
    app_server = WSGIServer(('0.0.0.0', 5000), app)
    app_server.serve_forever()
