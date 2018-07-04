import requests
from lxml import html
from datetime import datetime

proxies = { # if needed
    'https': 'http://172.17.10.2:3128'
}

headers = {
    'Connection':'close', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

#345 - NTU KhPI
#431 - KhNURE
#429 - Karazin KhNU
url = 'https://www.education.ua/universities/345/'

r = requests.get(url, proxies=proxies, headers=headers)

text = r.text

tree = html.fromstring(text)

ratings = tree.xpath('//meta[@itemprop="ratingValue"]')
dates = tree.xpath('//span[@itemprop="datePublished"]')

data = list()
for i in range(0, len(dates)):
    date = datetime.strptime(dates[i].get('content')[:-6], '%Y-%m-%dT%H:%M:%S')
    rating = int(ratings[i+1].get('content'))
    data.append((date, rating,) )

hist = dict()
for y in range(2009, 2019):
    hist[y] = dict()
    for r in range(0, 6):
        hist[y][r] = 0

for d in data:
    y = d[0].year
    hist[y][d[1]] += 1

    
for h in hist:
    print(h, end='\t')
    for r in range(0, 6):
        print(hist[h][r], end='\t')
    print()
