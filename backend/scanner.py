import datetime
import os
import re

import config

EXCLUDE_DIRS = (
        'extras',
        )

VIDEO_EXT = set((
        '.avi',
        '.mkv',
        '.mp4',
        ))

RIP_TYPE = set((
        'bdrip',
        'blu-ray\.rip',
        'blu-ray',
        'bluray',
        'brrip',
        'dvdivx',
        'dvdrip',
        'dvdscr',
        'hd',
        'hddvdrip',
        'hddvd',
        'hdre',
        'hdrip',
        'hdvdrip',
        'rerip',
        ))

DEF_TYPE = set((
        '1080i',
        '1080p',
        '480p',
        '720p',
        'a720',
        'imax',
        'stv',
        'ws',
        ))

VIDEO_ENCODE = set((
        'xvid',
        'divx',
        'x264',
        ))

AUDIO_ENCODE = set((
        '[0-9]+audio',
        '5.1ch',
        '6ch',
        'aac',
        'ac3',
        'dd20',
        'dd51',
        'dtshd',
        'dts',
        'dual-audio',
        'dual.audio',
        'dualaudio',
        'mp3',
        ))

RELEASE_TYPE = set((
        '[0-9]+cd',
        '[0-9]+th.anniversary',
        'directors.cut',
        'extended.cut',
        'collectors',
        'deluxe',
        'edition',
        'extended',
        'int',
        'internal',
        'limited',
        'proper',
        'readnfo',
        'remastered',
        'repack',
        'retail',
        'special',
        'superbit',
        'ultimate',
        'uncut',
        'unrated',
        'with.extras',
        'cc',
        'ce',
        'dc',
        'ec',
        'ee',
        'pe',
        're',
        'se',
        'ue',
        ))

LANG_TYPE = set((
        'cn',
        'danish',
        'finnish',
        'french',
        'hk',
        'jap',
        'japan',
        'norwegian',
        'swedish',
        ))

def has_video_files(filenames):
    '''Check if there is video in the filenames'''
    for filename in filenames:
        root, ext = os.path.splitext(filename)
        if ext in VIDEO_EXT:
            return True
    return False

def is_exclude_dir(dirpath):
    '''Check if a directory should be excluded'''
    if os.path.split(dirpath)[-1].lower() in EXCLUDE_DIRS:
        return True
    elif os.path.isfile(os.path.join(dirpath, '.bignore')):
        return True
    else:
        return False

def is_movie_dir(dirpath, filenames):
    '''Check if a directory is a valid movie directory'''
    if not is_exclude_dir(dirpath) and has_video_files(filenames):
        return True
    else:
        return False

def is_studly_caps(s):
    '''Check if a string is in studly caps'''
    if (s.islower() or s.isupper()) and s.isalpha():
        return False
    else:
        return True

def replace_token(strname, token):
    '''Replace matched tokens in a string with place holders'''
    m = re.search('(?<=[.-])%s(?=[.-])' % token, strname, re.IGNORECASE)
    if m and (m.group(0).isupper() or is_studly_caps(m.group(0))):
        match = strname[m.start(0):m.end(0)]
        strname = strname[:m.start(0)] + strname[m.end(0):]
    else:
        match = ''
    return strname, match

def strip_tokens(strname, tokens):
    '''Strip tokens from string'''
    match_tokens = []
    for token in tokens:
        strname, match = replace_token(strname, token)
        if match:
            match_tokens.append(match)
    return strname, match_tokens

def is_year(year):
    '''Check if a string represents a year'''
    if year.isdigit() and eval(year) >= 1900 and eval(year) <= datetime.datetime.now().year:
        return True
    else:
        return False

def extract_title_year(tokenlist):
    '''Extract title and year from title token list'''
    for i in range(len(tokenlist)-1, 0, -1):
        if is_year(tokenlist[i]):
            return tokenlist[0], eval(tokenlist[i])
    tokenlist = tokenlist[0].split('.')
    for i in range(len(tokenlist)-1, 0, -1):
        if is_year(tokenlist[i]):
            return ' '.join(tokenlist[:i]), eval(tokenlist[i])
    return ' '.join(tokenlist), None

def parse_release_name(basename):
    '''Parse release name into title and year'''
    strname = '.%s.' % basename
    strname, rip_type = strip_tokens(strname, RIP_TYPE)
    strname, def_type = strip_tokens(strname, DEF_TYPE)
    strname, video_encode = strip_tokens(strname, VIDEO_ENCODE)
    strname, audio_encode = strip_tokens(strname, AUDIO_ENCODE)
    strname, rel_type = strip_tokens(strname, RELEASE_TYPE)
    strname, lang_type = strip_tokens(strname, LANG_TYPE)
    strname = strname.replace('-', '.')
    strname = re.sub('\.\.+', '/', strname.strip('.'))
    tokenlist = strname.split('/')
    return extract_title_year(tokenlist)

def scan(dir=config.LIBRARY_DIR):
    ''' Scan directory for movies'''
    dirlist = []
    for dirpath, dirnames, filenames in os.walk(dir):
        if not is_movie_dir(dirpath, filenames):
            continue
        dirlist.append(dirpath)

    dirlist.sort()
    result = []
    for dirpath in dirlist:
        release = os.path.basename(dirpath)
        title, year = parse_release_name(release)
        result.append((dirpath, title, year))
    return result
