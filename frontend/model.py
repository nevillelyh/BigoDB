import datetime

import pymongo

class Model:
    def __init__(self):
        self.db = pymongo.Connection().bigodb

    def getMovies(self, sort, desc, filt = {}):
        result = {}
        for movie in self.db.Movie.find(filt,
                { 'ID':1, 'title':1, 'year':1, 'rating':1, 'votes':1, 'top 250 rank':1 }):
            result[movie['ID']] = movie
            result[movie['ID']]['item'] = []
            result[movie['ID']]['mtime'] = 0
        for item in self.db.Library.find():
            if item['ID'] not in result:
                continue
            result[item['ID']]['item'].append(item)
            if item['mtime'] > result[item['ID']]['mtime']:
                result[item['ID']]['mtime'] = item['mtime']
        result = result.values()

        attrkey = [ 'title', 'year', 'rating', 'votes', 'mtime', 'top 250 rank' ]
        
        reverse=False
        if desc != '0':
            reverse=True
        if sort in attrkey:
            result.sort(key=lambda item:item.get(sort, None), reverse=reverse)
        for item in result:
            item['mtime'] = datetime.datetime.fromtimestamp(item['mtime']).strftime('%Y/%m/%d')
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
