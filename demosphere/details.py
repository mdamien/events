import urldb
import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import itertools

events = json.load(open('data/index.json'))

for event in events:
    print(event['url'])
    html = urldb.get(event['url'])
    e = BeautifulSoup(html)
    all = itertools.chain(e.find_all('meta'), e.find_all('span'), e.find_all('a'), e.find_all('div'))
    for el in all:
        if 'itemprop' in el.attrs:
            if el.attrs['itemprop'] not in ('url','address','geo'):
                content = el.text.strip()
                if 'content' in el.attrs:
                    content = el.attrs['content']
                attr_name = el.attrs['itemprop']
                if attr_name == 'name':
                    attr_name = 'location'
                    if attr_name in event:
                        attr_name = 'title'
                event[attr_name] = content
    print(event['title'])

json.dump(events, open('data/details.json','w'), indent=2)