import urldb
import json
from pprint import pprint as pp
import itertools

URL = "http://paris.demosphere.eu/events.ics"

ALL = []

ics = urldb.get(URL)

for line in ics.split('\n'):
    if line.startswith('URL'):
        infos = {}
        infos['url'] = line.split(':',1)[1].strip()
        ALL.append(infos)

json.dump(ALL, open('data/index.json','w'), indent=2)

print(len(ALL))
