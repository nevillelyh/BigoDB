import unicodedata

import nltk
import pymongo

import scanner

tokenizer = nltk.tokenize.WordPunctTokenizer()

def update_vec(vec, t):
    if t not in vec:
        vec[t] = 1
    else:
        vec[t] += 1

def tokenize(s):
    n = unicode(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'))
    if len(s) != len(n):
        n = s
    t = tokenizer.tokenize(n)
    return t

def get_title_vector(movie):
    vec = {}
    for t in tokenize(movie['long imdb title']):
        update_vec(vec, t)

    for aka in movie.get('akas', []):
        title, sep, comment = aka.partition('::')
        for t in tokenize(title):
            update_vec(vec, t)

    return vec
