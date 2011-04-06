#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0], '..', 'lib')))

import web

import helper
import idxutil
import model

render = web.template.render('templates/',
        base='layout',
        globals={
            'column_head':helper.column_head,
            'time_repr':helper.time_repr,
            }
        )

urls = (
        '/', 'IndexView',
        '/top250/?', 'Top250View',
        '/g/([\w-]+)/?', 'GenreView',
        '/c/(\w+)/?', 'CountryView',
        '/l/(\w+)/?', 'LanguageView',
        '/m/(\d+)/?', 'MovieView',
        '/p/(\d+)/?', 'PersonView',
        '/s/([^/]+)?/?', 'SearchView',
        )

app = web.application(urls, globals())
model = model.Model()

if __name__ == '__main__':
    app.run()

class IndexView:
    def GET(self):
        get = web.input(s='m', d='1', v='l')
        result = model.getMovies(sort=get.s, desc=get.d)
        page = { 'get':get, 'list':result, 'top250':False, 'title':'BigoDB' }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class Top250View:
    def GET(self):
        get = web.input(s='t', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt={ 'top 250 rank':{ '$gt':0 } })
        page = { 'get':get, 'list':result, 'top250':True,
                'title':'BigoDB - Top 250' }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class GenreView:
    def GET(self, genre):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt={ 'genres':genre })
        page = { 'get':get, 'list':result, 'top250':False, 
                'title':'BigoDB - %s' % genre }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class CountryView:
    def GET(self, country):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt={ 'countries':country })
        page = { 'get':get, 'list':result, 'top250':False,
                'title':'BigoDB - %s' % country }
        if get.v == 'l':
            return render.ListView(page)
        else:
            return render.GridView(page)

class LanguageView:
    def GET(self, language):
        get = web.input(s='n', d='0', v='l')
        result = model.getMovies(sort=get.s, desc=get.d, filt={ 'languages':language })
        page = { 'get':get, 'list':result, 'top250':False,
                'title':'BigoDB - %s' % language }
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

class SearchView:
    def GET(self, query):
        get = web.input(q='')
        if get.q:
            print get.q
            raise web.seeother('/s/%s/' % get.q)
        movies = model.getMovies(sort='n', desc='0', filt=idxutil.build_query(query))
        persons = model.getPersons(filt=idxutil.build_query(query))
        page = { 'get':get, 'movie':movies, 'person': persons, 'title':'BigoDB Search' }
        return render.SearchView(page)
