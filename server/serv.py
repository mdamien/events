from flask import Flask, render_template, request
import json
import os, random

app = Flask(__name__)

def get_events():
    sources = [
        '10days/data/pages.json',
        'couchsurfing/cs.json',
        'eventbrite/data/pages.json',
        'meetups/data/events.json',
        'billetreduc/data/pages.json',
        'quefaire.paris.fr/data/pages.json',
    ]

    ALL = []
    L_ALL = 0
    for source in sources:
        source_dir = source.split('/',2)[0]
        with open('../'+source) as f:
            data = json.load(f)
            for x in data:
                x['source'] = source_dir 
            print('len(',source_dir,'):',len(data))
            random.shuffle(data)
            ALL += data[:30]
            L_ALL += len(data)

    print('len(all):',L_ALL)
    random.shuffle(ALL)
    return ALL

@app.route('/')
def index():
    return render_template('index.html', events=get_events())

if __name__ == '__main__':
    debug = os.getenv("PROD") == None
    app.run(port=8000, debug=debug)