import os
import sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0], '..', 'lib')))

import imdb
import pymongo

import config
import coverutil
import ffmpegutil
import idxutil
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

    mtime = os.path.getmtime(dirpath)
    db.Library.insert({
        'dirpath': dirpath,
        'ID': movie.getID(),
        'file': fileinfo,
        })

    # Add movie information
    if db.Movie.find_one({ 'ID': movie.getID() }):
        db.Movie.update({ 'ID': movie.getID() }, { '$set': { '_mtime': mtime } })
        return

    data = { 'ID': movie.getID(), '_mtime': mtime }
    for key in movie.keys():
        if type(movie[key]) is list:
            data[key] = []
            for item in movie[key]:
                if is_imdb_object(item):
                    if type(item).__name__ == 'Person':
                        item['_term_vector'] = idxutil.get_name_vector(item)
                    add_item(db[type(item).__name__], item)
                data[key].append(encode_object(item))
        else:
            data[key] = encode_object(movie[key])

    data['_term_vector'] = idxutil.get_title_vector(data)
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
    libmap = set()
    collmap = {
            'Movie': set(),
            'Person': set(),
            'Company': set(),
            }
    snapmap = set()

    result = scanner.scan()
    for dirpath, title, year in result:
        libmap.add(dirpath)

        item = db.Library.find_one({ 'dirpath':  dirpath })
        if not item:
            continue

        collmap['Movie'].add(item['ID'])

        movie = db.Movie.find_one({ 'ID': item['ID'] })
        if not movie:
            continue

        for key in movie.keys():
            if type(movie[key]) is list:
                for i in movie[key]:
                    if type(i) is dict and 'type' in i and 'ID' in i:
                        collmap[i['type']].add(i['ID'])
            elif type(movie[key]) is dict and 'type' in movie[key] and 'ID' in movie[key]:
                collmap[movie[key]['type']].add(movie[key]['ID'])

    count = 0
    for i in db.Library.find({}, { 'dirpath': 1, 'file': 1 }):
        if i['dirpath'] not in libmap:
            db.Library.remove({ 'dirpath': i['dirpath'] })
            count += 1
        for f in i['file']:
            if 'snapshot' in f:
                snapmap.add(f['snapshot'])

    print '[GC] Library: %d' % count

    for coll in collmap:
        count = 0
        for i in db[coll].find({}, { 'ID': 1 }):
            if i['ID'] not in collmap[coll]:
                db[coll].remove({ 'ID': i['ID'] })
                count += 1
        print '[GC] %s: %d' % (coll, count)

    count = 0
    snapdir = os.path.join(config.STATIC_DIR, 'snapshot')
    for entry in os.listdir(snapdir):
        snapfile = os.path.join(snapdir, entry)
        if entry not in snapmap and os.path.isfile(snapfile):
            os.remove(snapfile)
            count += 1
    print '[GC] Snapshot: %d' % count
