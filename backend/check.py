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
        if year:
            full_title = '%s (%d)' % (title, year)
        else:
            full_title = title

        item = db.Library.find_one({ 'dirpath': dirpath })
        if item:
            movie = db.Movie.find_one({ 'ID': item['ID'] })
            if movie:
                d = editdist.distance(full_title, movie['long imdb title'].encode('utf-8'))
                if float(d) / max(len(full_title), len(movie['long imdb title'])) > 0.2:
                    print ('[EDITDIST]\thttp://www.imdb.com/title/tt%s/\t%s ===> %s' % (movie['ID'], full_title, movie['long imdb title'])).encode('utf-8')
        else:
            print ('[UNKNOWN]\t%s ===> %s' % (dirpath, full_title)).encode('utf-8')

if __name__ == '__main__':
    main()
