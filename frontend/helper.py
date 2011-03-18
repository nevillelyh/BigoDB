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
