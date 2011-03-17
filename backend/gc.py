#!/usr/bin/env python

import os

import pymongo

import scanner

LIBRARY_DIR = '/home/public/Movies'

def main():
    db = pymongo.Connection().bigodb

    libmap = {}
    collmap = {
            'Movie': {},
            'Person': {},
            'Company': {},
            }

    result = scanner.scan(LIBRARY_DIR)
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

if __name__ == '__main__':
    main()
