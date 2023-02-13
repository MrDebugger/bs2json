from bs4 import BeautifulSoup as bs
import requests 
from bs2json import BS2Json

html = requests.get('https://webscraper.io/test-sites/e-commerce/static').text

soup = bs(html,'lxml')
converter = BS2Json(soup, 'lxml')

# testing one tag
json = converter.convert(class_='col-sm-4')
print(json, '*'*50, sep='\n', end='\n\n')

# testing more than one tags
jsonp = converter.convert_all(class_='col-sm-4')
print(jsonp, '*'*50, sep='\n', end='\n\n')

# testing more than one tags but joining same tags into one
tags = soup.findAll('a')
jsonp = converter.convert_all(tags, join=True)
print(jsonp, '*'*50, sep='\n', end='\n\n')

# changing labels for attributes and text
converter.labels(attributes='xxx',text='yyy')
tag = soup.find('title')
json = converter.convert(tag)
print(json,'*'*50,sep='\n',end='\n\n')
