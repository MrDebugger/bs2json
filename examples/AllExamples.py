from bs2json import bs2json
from bs4 import BeautifulSoup as bs
import requests 

html = requests.get('https://ijazurrahim.com').text

soup = bs(html,'lxml')
converter = bs2json()

# testing one tag
tag = soup.find(class_='home')
json = converter.convert(tag)
print(json)
print('*'*50)
print()

# testing more than one tags
tags = soup.findAll('a')
jsonp = converter.convertAll(tags)
print(jsonp)
print('*'*50)
print()

# testing more than one tags but joining same tags into one
tags = soup.findAll('a')
jsonp = converter.convertAll(tags,join=True)
print(jsonp)
print('*'*50)
print()

# changing labels for attributes and text
converter.labels(attributes='xxx',text='yyy')
tag = soup.find('h3')
json = converter.convert(tag)
print(json)
print('*'*50)
print()