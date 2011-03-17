#!/usr/bin/env python

import os

import pymongo

import scanner

LIBRARY_DIR = '/home/public/Movies'

def main():
    db = pymongo.Connection().bigodb

    idmap = {
            'Library': {},
            'Movie': {},
            'Person': {},
            'Company': {},
            }

    result = scanner.scan(LIBRARY_DIR)
    for dirpath, title, year in result:
        item = db.Library.find_one({ 'dirpath':  dirpath })
        if not item:
            continue

        idmap['Library'][item['ID']] = 1
        idmap['Movie'][item['ID']] = 1

        movie = db.Movie.find_one({ 'ID': item['ID'] })
        if not movie:
            continue

        for key in movie.keys():
            if type(movie[key]) is list:
                for i in movie[key]:
                    if type(i) is dict and 'type' in i and 'ID' in i:
                        idmap[i['type']][i['ID']] = 1
            elif type(movie[key]) is dict and 'type' in movie[key] and 'ID' in movie[key]:
                idmap[movie[key]['type']][movie[key]['ID']] = 1

    for coll in idmap:
        count = 0
        for i in db[coll].find({}, { 'ID': 1 }):
            if i['ID'] not in idmap[coll]:
                db[coll].remove({ 'ID': i['ID'] })
                count += 1
        print '[GC] %s: %d' % (coll, count)

if __name__ == '__main__':
    main()
