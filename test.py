import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "ext"))

from bs4 import BeautifulSoup
import urllib
import requests

query = 'linear search in python site:stackoverflow.com'
query = query.replace(" ", "+")


url = "https://www.google.com/search?q="+query+"&gbv=1&sei=YwHNVpHLOYiWmQHk3K24Cw"
print(url)
request = urllib.request.Request(url,headers={'User-Agent':'Sublime Text'})
r = urllib.request.urlopen(request).read()
soup = BeautifulSoup(r, "html.parser")

for item in soup.find_all('h3', attrs={'class' : 'r'}):
    url = item.a['href'][7:]
    break

response = urllib.request.urlopen(url).read()
soup = BeautifulSoup(response, "html.parser")

for item in soup.find_all('div', attrs={'class' : 'answer'}):
	try:
		print(item.find('pre').find('code').text)
		break
	except:
		continue