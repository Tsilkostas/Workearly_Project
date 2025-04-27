import sqlite3
import logging
from typing import Optional
from models import Movie, Director

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "movie_data.db"):
        self.db_path = db_path
        self._initialize_db()
        logger.info(f"Database initialized at {db_path}")
        
    def _initialize_db(self) -> None:
        """Create database tables if they don't exist"""
        try:
            with self._get_connection() as conn:
                with open("schema.sql") as f:
                    conn.executescript(f.read())
            logger.debug("Database schema initialized")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def upsert_movie(self, movie: Movie) -> int:
        """Insert or update a movie record
        
        Args:
            movie: Movie object to upsert
            
        Returns:
            ID of the inserted/updated record
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
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
                
                movie_id = cursor.fetchone()[0]
                logger.info(f"Upserted movie: {movie.title} (ID: {movie_id})")
                return movie_id
                
        except sqlite3.Error as e:
            logger.error(f"Failed to upsert movie {movie.title}: {e}")
            raise

    def upsert_director(self, director: Director) -> int:
        """Insert or update a director record
        
        Args:
            director: Director object to upsert
            
        Returns:
            ID of the inserted/updated record
        """
        try:
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
                
                director_id = cursor.fetchone()[0]
                logger.debug(f"Upserted director: {director.name} (ID: {director_id})")
                return director_id
                
        except sqlite3.Error as e:
            logger.error(f"Failed to upsert director {director.name}: {e}")
            raise

    def link_movie_director(self, movie_id: int, director_id: int) -> bool:
        """Create movie-director relationship
        
        Returns:
            True if relationship was created, False if it already existed
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO movie_directors (movie_id, director_id)
                    VALUES (?, ?)
                    ON CONFLICT DO NOTHING
                """, (movie_id, director_id))
                
                created = cursor.rowcount > 0
                if created:
                    logger.debug(f"Created movie-director link (Movie: {movie_id}, Director: {director_id})")
                return created
                
        except sqlite3.Error as e:
            logger.error(f"Failed to link movie {movie_id} with director {director_id}: {e}")
            raise