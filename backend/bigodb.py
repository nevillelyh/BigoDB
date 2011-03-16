import os
import time

import imdb
import pymongo

import nfoutil


db = pymongo.Connection().bigodb
ia = imdb.IMDb()
ia.set_proxy('http://localhost:8123/');

def search_movie(title, year):
    print '[DEBUG] search_movie()...',
    start = time.time()
    movie_result = ia.search_movie(title)
    end = time.time()
    print 'done in %f' % (end - start)
    candidate = []
    if year:
        for m in movie_result:
            if m['year'] == year:
                candidate.append(m)
    else:
        candidate = movie_result

    if len(candidate) == 0:
        return None

    for movie in candidate:
        print '[DEBUG] update()...',
        start = time.time()
        ia.update(movie)
        end = time.time()
        print 'done in %f' % (end - start)
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

    func_start = time.time()

    # Already added
    if db.Library.find_one({ 'dirpath': dirpath }):
        print '[SKIP] %s' % dirpath
        return

    # Look for IMDb link in .nfo
    nfo = nfoutil.get_nfo(dirpath)
    imdb_id = nfoutil.extract_imdb_id(nfo)

    if imdb_id:
        print '[DEBUG] get_movie()...',
        start = time.time()
        movie = ia.get_movie(imdb_id)
        end = time.time()
        print 'done in %f' % (end - start)
    else:
        movie = search_movie(title, year)

    if not movie:
        # Unidentified
        print '[UNIDENTIFIED] %s' % dirpath
        return

    print ('[MATCH] %s ===> %s' % (dirpath, movie['long imdb title'])).encode('utf-8')

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

    func_end = time.time()
    print '[DEBUG] add_movie()... done in %f' % (func_end - func_start)
    if func_end - func_start > 5:
        print '[DEBUG] sleep for 10 seconds'
        time.sleep(10)

def add_item(coll, item):
    '''Add an IMDBPy item to a collection'''

    if coll.find_one({ 'ID': item.getID() }):
        return

    data = { 'ID': item.getID(), }
    for key in item.keys():
        data[key] = encode_object(item[key])
    coll.insert(data)
