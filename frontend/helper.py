import datetime
import time

def column_head(get, top250=False):
    col_option = [
            ( 'n', 'Title', '0', ),
            ]
    if top250:
        col_option.append(('t', 'Rank', '1'))
    col_option += [
            ( 'y', 'Year', '1', ),
            ( 'r', 'Rating', '1', ),
            ( 'v', 'Votes', '1', ),
            ( 'm', 'Modified', '1', ),
            ]
    head = []
    for key, title, opt in col_option:
        arrow = ''
        if key == get.s:
            desc = ('1', '0')[get.d == '1']
            arrow = ('&uArr;', '&dArr;')[get.d == '1']
        else:
            desc = opt
        head.append(('%s %s' % (title, arrow), '?s=%s&d=%s&v=%s' % (key, desc, get.v)))
    return head

def time_repr(mtime):
    diff = int(time.time() - mtime)
    if diff < 60:
        return '%d second%s ago' % (diff, ('s', '')[diff<=1])
    elif diff < 3600:
        diff /= 60
        return '%d minute%s ago' % (diff, ('s', '')[diff<=1])
    elif diff < 86400:
        diff /= 3600
        return '%d hour%s ago' % (diff, ('s', '')[diff<=1])
    elif diff < 604800:
        diff /= 86400
        return '%d day%s ago' % (diff, ('s', '')[diff<=1])
    else:
        return datetime.datetime.fromtimestamp(mtime).strftime('%Y/%m/%d')
