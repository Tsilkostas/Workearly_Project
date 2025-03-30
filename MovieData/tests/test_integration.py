from MovieData.main import MovieDataApp
from MovieData.database import Database
from unittest.mock import patch
from pathlib import Path
import pytest

@pytest.fixture
def test_db(tmp_path):
    """Fixture that creates a test database"""
    db_path = tmp_path / "test_db.db"
    db = Database(db_path)
    # Initialize schema
    schema_path = Path(__file__).parent.parent / "schema.sql"
    with open(schema_path) as f:
        with db._get_connection() as conn:
            conn.executescript(f.read())
    return db

@patch("tmdb_client.TMDbClient.get_now_playing")
@patch("tmdb_client.TMDbClient.get_movie_details")
def test_full_workflow(mock_movie_details, mock_now_playing, test_db):
    # Setup mock data
    mock_now_playing.return_value = [{"id": 1, "title": "Test Movie"}]
    mock_movie_details.return_value = {
        "id": 1,
        "title": "Test Movie",
        "original_title": "Test Original",
        "overview": "A test film",
        "release_date": "2023-01-01",
        "credits": {
            "crew": [{"job": "Director", "id": 101, "name": "John Doe"}]
        }
    }
    
    # Test with mocked database
    app = MovieDataApp()
    app.db = test_db  # Inject test database
    
    app.fetch_and_store_movie_data()
    
    # Verify results
    with test_db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM movies WHERE id=1")
        assert cursor.fetchone()[0] == "Test Movie"