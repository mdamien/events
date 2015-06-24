import urldb
import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import itertools

URL = "https://www.eventbrite.com/d/france--paris/events/?crt=regular&page={page}" \
                "&slat=48.8566&slng=2.3522&sort=date"

ALL = []

i = 1
while True:
    i += 1
    html = urldb.get(URL.format(page=i))
    soup = BeautifulSoup(html)
    events = soup.find_all(class_='event-card')
    for e in events:
        infos = {}
        all = itertools.chain(e.find_all('meta'), e.find_all('span'))
        for el in all:
            print(str(el)[:30],'...')
            if 'itemprop' in el.attrs:
                if el.attrs['itemprop'] not in ('geo','location','address'):
                    content = el.text.strip()
                    if 'content' in el.attrs:
                        content = el.attrs['content']
                    infos[el.attrs['itemprop']] = content
        infos['title'] = e.find('h4').text.strip()
        #pp(infos)
        ALL.append(infos)

    print(len(events))

    json.dump(ALL, open('data/pages.json','w'), indent=2)

    if len(events) < 10:
        break

    print(len(ALL))
