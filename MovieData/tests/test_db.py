import pytest
from MovieData.database import Database

@pytest.fixture
def test_db(tmp_path):
    """Fixture that provides a clean test database"""
    db_path = tmp_path / "test_movie.db"
    db = Database(db_path)
    yield db
    db._get_connection().close()

def test_database_initialization(test_db):
    """Test that tables are created properly"""
    with test_db._get_connection() as conn:
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
        """)
        tables = {row[0] for row in cursor.fetchall()}
        assert tables == {'movies', 'directors', 'movie_directors'}

        # Verify movies table structure
        cursor.execute("PRAGMA table_info(movies)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {'id', 'tmdb_id', 'title', 'original_title', 
                         'description', 'release_date', 'last_updated'}