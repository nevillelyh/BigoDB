#!/usr/bin/env python

import web

import helper
import model

render = web.template.render('templates/', globals={
    'column_head': helper.column_head,
    })

urls = (
        '/', 'ListView',
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

class ListView:
    def GET(self):
        get = web.input(s='title', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d)
        page = { 'get': get, 'list': result, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class GenreView:
    def GET(self, genre):
        get = web.input(s='title', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'genres': genre })
        page = { 'get': get, 'list': result, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class CountryView:
    def GET(self, country):
        get = web.input(s='title', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'countries': country })
        page = { 'get': get, 'list': result, }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class LanguageView:
    def GET(self, language):
        get = web.input(s='title', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt = { 'languages': language })
        page = { 'get': get, 'list': result, }
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
