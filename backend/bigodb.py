import os
import imdb
import pymongo

import coverutil
import nfoutil

db = pymongo.Connection().bigodb
ia = imdb.IMDb()
# ia.set_proxy('http://localhost:8123/');

def search_movie(title, year):
    movie_result = ia.search_movie(title)
    candidate = []
    if year:
        for m in movie_result:
            if m.get('year', None) == year:
                candidate.append(m)
    else:
        candidate = movie_result

    if len(candidate) == 0:
        return None

    for movie in candidate:
        ia.update(movie)
    candidate.sort(reverse=True, key=lambda m:m.get('votes'))

    return candidate[0]

def is_imdb_object(obj):
    if type(obj) is imdb.Movie.Movie:
        return True
    elif type(obj) is imdb.Person.Person:
        return True
    elif type(obj) is imdb.Character.Character:
        return True
    elif type(obj) is imdb.Company.Company:
        return True
    else:
        return False

def encode_object(obj):
    if is_imdb_object(obj):
        return {
                'type': type(obj).__name__,
                'str': str(obj),
                'ID': obj.getID(),
                }
    else:
        return obj

def add_movie(dirpath, title, year):
    '''Add a movie to BigoDB'''

    # Already added
    if db.Library.find_one({ 'dirpath': dirpath }):
        return

    # Look for IMDb link in .nfo
    nfo = nfoutil.get_nfo(dirpath)
    imdb_id = nfoutil.extract_imdb_id(nfo)

    if imdb_id:
        movie = ia.get_movie(imdb_id)
    else:
        movie = search_movie(title, year)

    # Unidentified
    if not movie:
        print '[UNKNOWN] %s' % dirpath
        return

    db.Library.insert({
        'dirpath': dirpath,
        'ID': movie.getID(),
        'mtime': os.path.getmtime(dirpath),
        })

    if db.Movie.find_one({ 'ID': movie.getID() }):
        return

    data = { 'ID': movie.getID(), }
    for key in movie.keys():
        if type(movie[key]) is list:
            data[key] = []
            for item in movie[key]:
                if is_imdb_object(item):
                    add_item(db[type(item).__name__], item)
                data[key].append(encode_object(item))
        else:
            data[key] = encode_object(movie[key])
    db.Movie.insert(data)
    coverutil.fetch_cover(movie)

    if not year:
        year = 0
    print ('[MATCH] %s %s (%d) ===> %s (%d)' % (dirpath, title, year, movie['title'], movie['year'])).encode('utf-8')

def add_item(coll, item):
    '''Add an IMDBPy item to a collection'''

    if coll.find_one({ 'ID': item.getID() }):
        return

    data = { 'ID': item.getID(), }
    for key in item.keys():
        data[key] = encode_object(item[key])
    coll.insert(data)
