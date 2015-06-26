import urldb
import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import itertools

BASE_URL = "http://www.billetreduc.com"
URL = BASE_URL+"/s.htm?gp=1&Lpg={page}"

ALL = []

i = 0
while True:
    i += 1
    html = urldb.get(URL.format(page=i))
    soup = BeautifulSoup(html)
    events = soup.find_all(class_='leEvt')
    for e in events:
        infos = {}
        img = e.find('img')
        if img:
            infos['img'] = img.attrs['src']
        titre = e.find(class_='leTitre')
        infos['url'] = BASE_URL+titre.find('a').attrs['href']
        infos['title'] = titre.text.strip()
        infos['description'] = e.find(class_='leDescriptif').contents[2].strip()
        infos['price'] = e.find(class_='bpprix').contents[0].strip()
        pp(infos)
        ALL.append(infos)

    print(len(events))

    json.dump(ALL, open('data/pages.json','w'), indent=2)

    if len(events) < 40:
        break

    print(len(ALL))
