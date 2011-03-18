#!/usr/bin/env python

import web

import helper
import model

render = web.template.render('templates/', globals={
    'column_head':helper.column_head,
    })

urls = (
        '/', 'IndexView',
        '/top250/?', 'Top250View',
        '/g/([\w-]+)/?', 'GenreView',
        '/c/(\w+)/?', 'CountryView',
        '/l/(\w+)/?', 'LanguageView',
        '/m/(\d+)/?', 'MovieView',
        '/p/(\d+)/?', 'PersonView',
        )

app = web.application(urls, globals())
model = model.Model()

if __name__ == '__main__':
    app.run()

class IndexView:
    def GET(self):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d)
        page = { 'get':get, 'list':result, 'top250':False, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class Top250View:
    def GET(self):
        get = web.input(s='t', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'top 250 rank':{ '$gt':0 } })
        page = { 'get':get, 'list':result, 'top250':True, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class GenreView:
    def GET(self, genre):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'genres':genre })
        page = { 'get':get, 'list':result, 'top250':False, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class CountryView:
    def GET(self, country):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'countries':country })
        page = { 'get':get, 'list':result, 'top250':False, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class LanguageView:
    def GET(self, language):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'languages':language })
        page = { 'get':get, 'list':result, 'top250':False, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class MovieView:
    def GET(self, imdb_id):
        result = model.getMovie(imdb_id)
        return render.MovieView(result)

class PersonView:
    def GET(self, imdb_id):
        result = model.getPerson(imdb_id)
        return render.PersonView(result)
