#!/usr/bin/env python

import pymongo

import nfoutil
import scanner

def main():
    db = pymongo.Connection().bigodb
    result = scanner.scan()
    for dirpath, title, year in result:
        item = db.Library.find_one({ 'dirpath': dirpath })
        if not item:
            continue

        nfo = nfoutil.get_nfo(dirpath)
        imdb_id = nfoutil.extract_imdb_id(nfo)

        if not imdb_id:
            print 'echo "http://www.imdb.com/title/tt%s/" > %s/.bigodb.nfo' % (item['ID'], dirpath)

if __name__ == '__main__':
    main()
