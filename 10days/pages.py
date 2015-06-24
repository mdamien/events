import urldb
import json
from bs4 import BeautifulSoup

URL = "http://www.tendaysinparis.com/events/list/?action=tribe_list&tribe_paged={page}&tribe_event_display=list"

ALL = []

i = 1
while True:
    i += 1
    html = urldb.get(URL.format(page=i))
    soup = BeautifulSoup(html)
    vevent = soup.find_all(class_='vevent')
    for event in vevent:
        infos = {}
        a = event.find(class_='url')
        infos['url'] = a.attrs['href']
        infos['title'] = a.text.strip()
        infos['date-start'] = event.find('span',
                {'class':'value-title'}).attrs['title']
        date_end = event.find('span',
                {'class':'date-end dtend'})
        if date_end:
            date_end = date_end.find('span')
            infos['date-end'] = date_end.attrs['title']
        infos['organizer'] = event.find(class_='author fn org').text.strip()
        loc = event.find(class_='tribe-events-address')
        if loc:
            infos['location'] = loc.text.strip()
        img = event.find('img')
        if img:
            infos['img'] = img.attrs['src']
        print(infos)
        ALL.append(infos)

    if len(vevent) < 15:
        break

    print(len(ALL))

json.dump(ALL, open('data/pages.json','w'), indent=2)