#!/usr/bin/env python

import web

import model

render = web.template.render('templates/')

urls = (
        '/', 'ListView',
        '/l/?', 'ListView',
        '/m/(\d+)/?', 'MovieView',
        '/p/(\d+)/?', 'PersonView',
        )

app = web.application(urls, globals())
model = model.Model()

if __name__ == '__main__':
    app.run()

class ListView:
    def GET(self):
        get = web.input(sort='title', desc='off')
        result = model.getMovies(sort=get.sort, desc=get.desc)
        page = { 'get': get, 'list': result, }
        return render.ListView(page)

class MovieView:
    def GET(self, imdb_id):
        result = model.getMovie(imdb_id)
        return render.MovieView(result)

class PersonView:
    def GET(self, imdb_id):
        result = model.getPerson(imdb_id)
        return render.PersonView(result)
