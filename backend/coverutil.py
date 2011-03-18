import os
import urllib2

import config

def fetch_url(url, path):
    if os.path.isfile(path):
        return
    fin = urllib2.urlopen(url)
    fout = open(path, 'w')
    fout.write(fin.read())
    fout.close()
    fin.close()

def fetch_cover(movie):
    if 'cover url' in movie:
        root, ext = os.path.splitext(movie['cover url'])
        dest = os.path.join(config.STATIC_DIR, 'cover_small', '%s%s' % (movie['ID'], ext))
        fetch_url(movie['cover url'], dest)
    if 'full-size cover url' in movie:
        root, ext = os.path.splitext(movie['full-size cover url'])
        dest = os.path.join(config.STATIC_DIR, 'cover_full', '%s%s' % (movie['ID'], ext))
        fetch_url(movie['full-size cover url'], dest)
