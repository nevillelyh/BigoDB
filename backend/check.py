#!/usr/bin/env python

import os

import editdist
import pymongo

import scanner

db = pymongo.Connection().bigodb

def is_audio(stream):
    if ' Audio: ' in stream:
        return True
    else:
        return False

def is_surround(stream):
    if ' 5.1, ' in stream and ('ac3' in stream or 'dca' in stream):
        return True
    else:
        return False

def is_subtitle(stream):
    if ' Subtitle: ' in stream:
        return True
    else:
        return False

def check_stream():
    for item in db.Library.find():
        for f in item['file']:
            stat = {'audio':0, 'subtitle':0, 'surround':0}
            report = []
            for s in f['info']['stream']:
                report.append(s)
                if is_audio(s):
                    stat['audio'] += 1
                    if is_surround(s):
                        stat['surround'] += 1
                elif is_subtitle(s):
                    stat['subtitle'] += 1
            if stat['surround'] == 0 or stat['subtitle'] > 1:
                print '[STREAM] %s' % f['path']
                for s in f['info']['stream']:
                    print '\t%s' % s

def check_title():
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
                    print ('[EDITDIST] %s %s ===> %s' % (movie['ID'], original, movie['long imdb title'])).encode('utf-8')
        else:
            print '[UNKNOWN] %s ===> %s' % (dirpath, original)

def main():
    check_stream()
    # check_title()

if __name__ == '__main__':
    main()
