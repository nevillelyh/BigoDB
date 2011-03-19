import os
import imdb
import pymongo

import coverutil
import ffmpegutil
import nfoutil
import scanner

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

    if not year:
        year = 0
    print ('[MATCH] %s %s (%d) ===> %s (%d)' % (dirpath, title, year, movie['title'], movie['year'])).encode('utf-8')

    # Take snapshot
    fileinfo = ffmpegutil.take_release_snapshot(dirpath)

    db.Library.insert({
        'dirpath': dirpath,
        'ID': movie.getID(),
        'mtime': os.path.getmtime(dirpath),
        'file': fileinfo,
        })

    # Add movie information
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

    # Fetch cover
    coverutil.fetch_cover(data)

def add_item(coll, item):
    '''Add an IMDBPy item to a collection'''

    if coll.find_one({ 'ID': item.getID() }):
        return

    data = { 'ID': item.getID(), }
    for key in item.keys():
        data[key] = encode_object(item[key])
    coll.insert(data)

def scan():
    result = scanner.scan()
    for dirpath, title, year in result:
        add_movie(dirpath, title, year)

def gc():
    libmap = {}
    collmap = {
            'Movie': {},
            'Person': {},
            'Company': {},
            }

    result = scanner.scan()
    for dirpath, title, year in result:
        libmap[dirpath] = 1

        item = db.Library.find_one({ 'dirpath':  dirpath })
        if not item:
            continue

        collmap['Movie'][item['ID']] = 1

        movie = db.Movie.find_one({ 'ID': item['ID'] })
        if not movie:
            continue

        for key in movie.keys():
            if type(movie[key]) is list:
                for i in movie[key]:
                    if type(i) is dict and 'type' in i and 'ID' in i:
                        collmap[i['type']][i['ID']] = 1
            elif type(movie[key]) is dict and 'type' in movie[key] and 'ID' in movie[key]:
                collmap[movie[key]['type']][movie[key]['ID']] = 1

    count = 0
    for i in db.Library.find({}, { 'dirpath': 1 }):
        if i['dirpath'] not in libmap:
            db.Library.remove({ 'dirpath': i['dirpath'] })
            count += 1
    print '[GC] Library: %d' % count

    for coll in collmap:
        count = 0
        for i in db[coll].find({}, { 'ID': 1 }):
            if i['ID'] not in collmap[coll]:
                db[coll].remove({ 'ID': i['ID'] })
                count += 1
        print '[GC] %s: %d' % (coll, count)
