#!/usr/bin/env python

import os

import bigodb
import config
import scanner

def main():
    result = scanner.scan(config.LIBRARY_DIR)
    for dirpath, title, year in result:
        bigodb.add_movie(dirpath, title, year)

if __name__ == '__main__':
    main()
