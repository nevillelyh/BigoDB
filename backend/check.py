#!/usr/bin/env python

import os

import editdist
import pymongo

import bigodb
import scanner

LIBRARY_DIR = '/home/public/Movies'

def main():
    db = pymongo.Connection().bigodb
    result = scanner.scan(LIBRARY_DIR)
    for dirpath, title, year in result:
        item = db.Library.find_one({ 'dirpath': dirpath })
        if item:
            movie = db.Movie.find_one({ 'ID': item['ID'] })
            if movie:
                if year:
                    original = '%s (%d)' % (title, year)
                    matched = movie['long imdb title']
                else:
                    original = title
                    matched = movie['title']
                d = editdist.distance(original, matched.encode('utf-8'))
                if float(d) / max(len(original), len(matched)) > 0.2:
                    print ('[EDITDIST]\thttp://www.imdb.com/title/tt%s/\t%s ===> %s' % (movie['ID'], original, matched)).encode('utf-8')
        else:
            print '[UNKNOWN]\t%s ===> %s' % (dirpath, original)

if __name__ == '__main__':
    main()
