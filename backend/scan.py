#!/usr/bin/env python

import os

import bigodb
import scanner

LIBRARY_DIR = '/home/public/Movies'

def main():
    result = scanner.scan(LIBRARY_DIR)
    for dirpath, title, year in result:
        bigodb.add_movie(dirpath, title, year)

if __name__ == '__main__':
    main()
