-- schema.sql
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    tmdb_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    original_title TEXT NOT NULL,
    description TEXT,
    release_date TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS directors (
    id INTEGER PRIMARY KEY,
    tmdb_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    imdb_id TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movie_directors (
    movie_id INTEGER NOT NULL,
    director_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (director_id) REFERENCES directors(id)
);