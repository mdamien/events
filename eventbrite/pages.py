import urldb
import json
from bs4 import BeautifulSoup

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
        infos['title'] = e.find('h4').text.strip()
        print(infos)
        ALL.append(infos)

    print(len(events))
    if len(events) < 10:
        break

    print(len(ALL))

json.dump(ALL, open('data/pages.json','w'), indent=2)