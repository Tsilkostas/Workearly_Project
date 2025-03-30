
import sqlite3
from MovieData.models import Movie, Director

class Database:
    def __init__(self, db_path: str = "movie_data.db"):
        self.db_path = db_path
        self._initialize_db()
        
    def _initialize_db(self):
        """Create database tables if they don't exist"""
        with self._get_connection() as conn:
            with open("schema.sql") as f:
                conn.executescript(f.read())
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def upsert_movie(self, movie: Movie) -> int:
        """Insert or update a movie record"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO movies (tmdb_id, title, original_title, description, release_date)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    title = excluded.title,
                    original_title = excluded.original_title,
                    description = excluded.description,
                    release_date = excluded.release_date,
                    last_updated = CURRENT_TIMESTAMP
                RETURNING id
            """, (movie.tmdb_id, movie.title, movie.original_title, 
                  movie.description, movie.release_date))
            print(f"Upserting movie: {movie.title}")
            return cursor.fetchone()[0]
    
    def upsert_director(self, director: Director) -> int:
        """Insert or update a director record"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO directors (tmdb_id, name, imdb_id)
                VALUES (?, ?, ?)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    name = excluded.name,
                    imdb_id = excluded.imdb_id,
                    last_updated = CURRENT_TIMESTAMP
                RETURNING id
            """, (director.tmdb_id, director.name, director.imdb_id))
            return cursor.fetchone()[0]
    
    def link_movie_director(self, movie_id: int, director_id: int) -> None:
        """Create movie-director relationship"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO movie_directors (movie_id, director_id)
                VALUES (?, ?)
            """, (movie_id, director_id))