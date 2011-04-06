db.Library.ensureIndex({ ID: 1 } );
db.Library.ensureIndex({ dirpath: 1 });

db.Movie.ensureIndex({ ID: 1 });

db.Movie.ensureIndex({ countries: 1 });
db.Movie.ensureIndex({ genres: 1 });
db.Movie.ensureIndex({ languages: 1 });

db.Movie.ensureIndex({ title: 1 });
db.Movie.ensureIndex({ year: 1 });
db.Movie.ensureIndex({ rating: 1 });
db.Movie.ensureIndex({ votes: 1 });
db.Movie.ensureIndex({ 'top 250 rank': 1 });

db.Movie.ensureIndex({ _term_vector: 1 });
db.Movie.ensureIndex({ _mtime: 1 });

db.Person.ensureIndex({ ID: 1 });
db.Person.ensureIndex({ _term_vector: 1 });

db.Company.ensureIndex({ ID: 1 });
