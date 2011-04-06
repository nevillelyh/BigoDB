import pymongo

import helper

class Model:
    def __init__(self):
        self.db = pymongo.Connection().bigodb

    def getMovies(self, sort, desc, filt = {}):
        keymap = {
                'n':'title',
                'y':'year',
                'r':'rating',
                'v':'votes',
                'm':'_mtime',
                't':'top 250 rank'
                }

        if desc == 0:
            order = pymongo.ASCENDING
        else:
            order = pymongo.DESCENDING

        result = []
        for movie in self.db.Movie.find(filt, {
            'ID':1,
            'title':1,
            'long imdb title':1,
            'year':1,
            'rating':1,
            'votes':1,
            'top 250 rank':1,
            'cover url':1,
            '_mtime':1,
            }).sort(keymap[sort], order):
            if 'cover url' not in movie:
                item = self.db.Library.find_one({ 'ID': movie['ID'] })
                snapshot = item.get('file', [{}])[0].get('snapshot', None)
                if snapshot:
                    movie['snapshot'] = snapshot
            result.append(movie)
        return result

    def getPersons(self, filt = {}):
        result = []
        for person in self.db.Person.find(filt):
            result.append(person)
        return result

    def getMovie(self, imdb_id):
        movie = self.db.Movie.find_one({ 'ID': imdb_id })
        if not movie:
            return None

        movie['item'] = []
        for item in self.db.Library.find({ 'ID': imdb_id }):
            movie['item'].append(item)

        return movie

    def getPerson(self, imdb_id):
        person = self.db.Person.find_one({ 'ID': imdb_id })
        if not person:
            return None

        for role in ['director', 'writer', 'producer', 'cast']:
            person[role] = []
            for movie in self.db.Movie.find( { '%s.ID' % role: imdb_id }, { 'ID':1, 'title':1, 'year':1, }) .sort('year', pymongo.DESCENDING):
                person[role].append(movie)

        return person
