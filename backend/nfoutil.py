import os
import re

def get_nfo(dirpath):
    lines = []
    dlist = os.listdir(dirpath)
    dlist.sort()
    for entry in dlist:
        root, ext = os.path.splitext(entry)
        if ext.lower() != '.nfo':
            continue

        path = os.path.join(dirpath, entry)
        if not os.path.isfile(path):
            continue

        f = open(path, 'r')
        lines += f.readlines()
        f.close()
    return '\n'.join(lines)

def extract_imdb_id(nfo):
    patterns = [
            '(?<=.imdb.com/title/tt)[0-9]+',
            '(?<=.imdb.com/Title\?)[0-9]+',
            '(?<=.imdb.com/Details\?)[0-9]+',
            ]

    for p in patterns:
        m = re.search(p, nfo)
        if m:
            return m.group(0)
    return None
