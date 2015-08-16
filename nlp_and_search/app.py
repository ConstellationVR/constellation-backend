from flask import Flask

import flask, re

from nltk.stem import *
from nltk.corpus import wordnet

from alchemyapi import AlchemyAPI
import socket 
import urllib, json

app = Flask(__name__)

alchemyapi = AlchemyAPI()

bing_base_url = 'http://api.bing.com/osjson.aspx?query='

@app.route('/stem/<query>')
def stem(query):
    quer = query.split()
    stemmer = SnowballStemmer("english")

    single = [stemmer.stem(plural) for plural in quer]

    result = {'stemmed': single}

    return flask.jsonify(**result)

@app.route('/interpret/<query>')
def interpret(query):
    response = alchemyapi.concepts('text', query)

    res = {}
    i = 0

    if len(response['concepts'])>0:
        for concept in response['concepts']:
            con = {}
            con['text'] = concept['text']
            con['relevance'] = concept['relevance']

            dbpedia_json_url = concept['dbpedia'].replace('/resource/', '/data/')+'.json'

            resp = urllib.urlopen(dbpedia_json_url)
            data = json.loads(resp.read())

            abstract = []
            for dat in data[concept['dbpedia']]['http://dbpedia.org/ontology/abstract']:
                if dat['lang']=='en':
                    abstract = dat
            con['abstract'] = abstract['value']
            res[str(i)] = con
            i+=1
        return flask.jsonify(**res)
    else:
        synsets = wordnet.synsets(query)
        defs = {}

        i = 0
        for synset in synsets[:3]:
            de = {}

            de['name'] = re.sub('\..+','', synset.name())

            de['lexical_type'] = re.sub('\..+','', synset.lexname())
            de['definition'] = synset.definition()

            defs[i] = de
            i+=1

        resp = urllib.urlopen(bing_base_url+query)
        data = json.loads(resp.read())

        res['bing'] = data[1][:5]
        res['definitions'] = defs

        return flask.jsonify(**res)

if __name__ == "__main__":
    app.debug = True
    app.run(host=socket.gethostbyname(socket.gethostname()))
