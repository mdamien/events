import urldb
import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import itertools

BASE_URL = "http://quefaire.paris.fr"
URL = BASE_URL+"/all/0/{count}"

ALL = []

i = 0
while True:
    html = urldb.get(URL.format(count=i))
    soup = BeautifulSoup(html)
    events = soup.find_all(class_='result-section')
    for e in events:
        infos = {}
        link = e.find('h1')
        if link:
            link = link.find('a')
            infos['url'] = link.attrs['href']
            infos['title'] = link.text.strip()
            img = e.find('img')
            if img:
                infos['img'] = img.attrs['src']
            infos['description'] = e.find(class_='first-intro').text.strip()
            price = e.find(class_='prix')
            if price:
                infos['price'] = price.text.strip()

            all = itertools.chain(e.find_all('meta'), e.find_all('span'), e.find_all('a'))
            for el in all:
                if 'itemprop' in el.attrs:
                    if el.attrs['itemprop'] not in ('url','name'):
                        content = el.text.strip()
                        if 'content' in el.attrs:
                            content = el.attrs['content']
                        infos[el.attrs['itemprop']] = content
            ALL.append(infos)

    print(len(events))

    json.dump(ALL, open('data/pages.json','w'), indent=2)

    if len(events) < 11:
        break

    print(len(ALL))

    i += 10
