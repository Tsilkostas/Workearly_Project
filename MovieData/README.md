# MovieData Application

Fetches current movies in Greek theaters from TMDb API and stores them in a SQLite database with director information.

## Features
- Retrieves movies currently playing in Greek theaters
- Stores complete movie information including:
  - Title and original title
  - Description
  - Release date
  - Director information with IMDb links
- Updates database with latest information on each run
- Simple command-line interface

## Requirements
- pip install -r requirements.txt
- TMDb API key (default key included)

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

## Usage
Run the application with:
    ```bash
    python run.py

This will:

1. Fetch movies currently playing in Greece from TMDb

2. Store them in movie_data.db (SQLite database)

3. Print progress to console

## Configuration
By default, the application uses an included API key. To use your own:
1. Create a .env file in the project root
2. Add your key:
TMDB_API_KEY=your_api_key_here

## Database Verification
Basic Checks
sqlite3 movie_data.db
-- Count movies
SELECT COUNT(*) FROM movies;

-- Count directors
SELECT COUNT(*) FROM directors;

-- Verify director links
SELECT COUNT(*) FROM movie_directors;

-- Verify director links
SELECT COUNT(*) FROM movie_directors;

Sample Data
SELECT 
    m.title AS movie_title,
    d.name AS director,
    'https://www.imdb.com/name/' || d.imdb_id AS imdb_link
FROM movies m
JOIN movie_directors md ON m.id = md.movie_id
JOIN directors d ON d.id = md.director_id
LIMIT 5;

Data Quality Checks
-- Movies with missing descriptions
SELECT title FROM movies WHERE description IS NULL OR description = '';

-- Directors without IMDb links
SELECT name FROM directors WHERE imdb_id IS NULL OR imdb_id = '';

-- Verify no duplicate movies
SELECT tmdb_id, COUNT(*) FROM movies GROUP BY tmdb_id HAVING COUNT(*) > 1;

Database Schema
The application uses the following schema (stored in schema.sql):
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

Troubleshooting
If you get API errors, verify your internet connection

Delete movie_data.db to reset the database

Some movies/directors might have incomplete data from TMDb

Run tests
python -m pytest