def column_head(get):
    col_option = (
            ( 'title', 'Title', '0', ),
            ( 'year', 'Year', '1', ),
            ( 'rating', 'Rating', '1', ),
            ( 'votes', 'Votes', '1', ),
            ( 'mtime', 'Modified', '1', ),
            )
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
