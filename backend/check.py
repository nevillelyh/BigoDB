#!/usr/bin/env python

import os

import editdist
import pymongo

import scanner

def main():
    db = pymongo.Connection().bigodb
    result = scanner.scan()
    for dirpath, title, year in result:
        if year:
            original = '%s (%d)' % (title, year)
        else:
            original = title

        item = db.Library.find_one({ 'dirpath': dirpath })
        if item:
            movie = db.Movie.find_one({ 'ID': item['ID'] })
            if movie:
                if year:
                    matched = movie['long imdb title']
                else:
                    matched = movie['title']
                d = editdist.distance(original.lower(), matched.lower().encode('utf-8'))
                if float(d) / max(len(original), len(matched)) > 0.2:
                    print ('[EDITDIST]\t%s\t%s ===> %s' % (movie['ID'], original, movie['long imdb title'])).encode('utf-8')
        else:
            print '[UNKNOWN]\t%s ===> %s' % (dirpath, original)

if __name__ == '__main__':
    main()
