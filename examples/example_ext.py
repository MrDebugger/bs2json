from bs4 import BeautifulSoup
from bs2json import install
install()

html = '<html><head><title>Page Title</title></head><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>'
soup = BeautifulSoup(html, 'lxml')

# convert return of the find method to json
print(soup.find('body').to_json())
# convert the soup object to json
print(soup.to_json())
# convert any tag to json
print(soup.body.to_json())