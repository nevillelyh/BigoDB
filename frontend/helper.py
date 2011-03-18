def column_head(get, top250=False):
    col_option = [
            ( 'title', 'Title', '0', ),
            ]
    if top250:
        col_option.append(('top 250 rank', 'Rank', '1'))
    col_option += [
            ( 'year', 'Year', '1', ),
            ( 'rating', 'Rating', '1', ),
            ( 'votes', 'Votes', '1', ),
            ( 'mtime', 'Modified', '1', ),
            ]
    head = []
    for key, title, opt in col_option:
        arrow = ''
        if key == get.s:
            desc = ('1', '0')[get.d == '1']
            arrow = ('&uArr;', '&dArr;')[get.d == '1']
        else:
            desc = opt
        if top250:
            head.append(('%s %s' % (title, arrow), '?s=%s&d=%s' % (key, desc)))
        else:
            head.append(('%s %s' % (title, arrow), '?s=%s&d=%s&v=%s' % (key, desc, get.v)))
    return head
