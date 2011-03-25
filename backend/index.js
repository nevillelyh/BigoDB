db.Library.ensureIndex({ ID: 1 } );
db.Library.ensureIndex({ dirpath: 1 });
db.Movie.ensureIndex({ ID: 1 });
db.Movie.ensureIndex({ countries: 1 });
db.Movie.ensureIndex({ genres: 1 });
db.Movie.ensureIndex({ languages: 1 });
db.Movie.ensureIndex({ title_vector: 1 });
db.Person.ensureIndex({ ID: 1 });
db.Company.ensureIndex({ ID: 1 });
