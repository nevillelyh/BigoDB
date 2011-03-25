import unicodedata

import nltk

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
    return [t.lower() for t in tokenizer.tokenize(n)]

def get_title_vector(movie):
    vec = {}
    for t in tokenize(movie['long imdb title']):
        update_vec(vec, t)

    for aka in movie.get('akas', []):
        title, sep, comment = aka.partition('::')
        for t in tokenize(title):
            update_vec(vec, t)

    return vec

def build_query(query):
    query = query.replace('+', ' ')
    q = {}
    for t in tokenize(query):
        q['title_vector.%s' % t] = {'$gt':0}
    return q
