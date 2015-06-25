#! /usr/bin/python2

from meetupapi import *
from pprint import pprint as pp
import os, sys
import json

envkey = os.environ.get('MEETUP_APIKEY')
if not envkey:
    print('oops, you forgot the api key as an env var')
    sys.exit(0)

api = Meetup(envkey)

ALL = []

for i in range(10):
    print(i)
    r = api._fetch('2/open_events',lat=48.858093,lon=2.294694,page=100, offset=i)

    ALL += r['results']

with open('data/events.json','w') as f:
    json.dump(ALL, f, indent=2)