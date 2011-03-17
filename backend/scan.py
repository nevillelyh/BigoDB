#!/usr/bin/env python

import os

import bigodb
import scanner

LIBRARY_DIR = '/home/public/Movies'

def main():
    result = scanner.scan(LIBRARY_DIR)
    count = 0
    total = len(result)
    for dirpath, title, year in result:
        count += 1
        msg = '[%4d/%4d] %s ===> "%s"' % (count, total, os.path.basename(dirpath), title)
        if year:
            msg += ' (%d)' % year
        print msg
        bigodb.add_movie(dirpath, title, year)

if __name__ == '__main__':
    main()
