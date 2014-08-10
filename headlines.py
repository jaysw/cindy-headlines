import json
import uuid
import time
from bs4 import BeautifulSoup
import string
import os, sys, getpass
from os import path
import re
import nltk
import random

from flask import Flask, render_template

app = Flask('cindyheadlines')

if not hasattr(app, 'extensions'):
    app.extensions = {}
app.extensions['cindy'] = {
    'headlines': None,
    'model': None
}


def read_headline():
    with open('headlines.txt') as f:
        for idx, line in enumerate(f):
            if not line:
                continue
            yield BeautifulSoup(line).text + '.'  # this might help the sentence tokenizer


def get_words():
    print "fetching words"
    words = []
    for post in read_headline():
        for sentence in nltk.sent_tokenize(post):
            for word in nltk.word_tokenize(sentence):
                words.append(word.encode('utf8', 'ignore'))
    print "%i words" % len(words)
    return words


def post_prep(post):
        #post = re.sub(r" ([!\.:'\";,?])", r"\1", post).replace('( ', '(').replace(' * ', '*')
        #post = re.sub(r" (n't|'ll)", r'\1', post)
        return post


def headlines():
    return app.extensions['cindy']['headlines']


def model():
    return app.extensions['cindy']['model']


def get_headline():
    lines = app.extensions['cindy']['headlines'].values()
    model = app.extensions['cindy']['model']
    ctx = [random.choice(lines).split()[0]]
    words = ' '.join(w.decode('utf-8', 'ignore') for w in model.generate(20, context=ctx))
    sents = words.split('.')
    sents.sort(key=lambda s: len(s), reverse=True)
    hl = sents[0]
    hl = hl.replace(" 's", "'s").replace(' ,', ',').replace(' :', ':')\
            .replace(' ?', '?').replace(" 'm", "'m")\
            .replace(' !', '!').strip()
    tokes = hl.split()
    return tokes[0].capitalize() + ' '  + ' '.join(tokes[1:])


def get_model():
    if not app.extensions['cindy']['model']:
        words = get_words()
        print "Generating model...",
        text = nltk.Text(words)
        estimator = lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)
        model = nltk.model.NgramModel(3, text, estimator=estimator)
        app.extensions['cindy']['model'] = model
        return model


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def bleh():
    return 'blargh!', 404


@app.route('/guess/<uu>')
def guess(uu):
    d = {"result": uu in headlines()}
    return json.dumps(d), 200, {'content-type': 'text/json'}

@app.route('/q')
def question():
    posts = {}
    uu = random.choice(headlines().keys())
    posts[uu] = headlines()[uu]
    posts[str(uuid.uuid4())] = get_headline()
    return json.dumps(posts), 200, {'content-type': 'text/json'}


_model = get_model()
print 'done'
print "reading headline data..",
with open('headlines.txt') as fin:
    app.extensions['cindy']['headlines'] = {str(uuid.uuid4()): BeautifulSoup(h.strip()).text  for h in fin}
print "done"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


