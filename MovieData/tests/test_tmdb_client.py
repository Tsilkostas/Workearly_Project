
import pytest
from unittest.mock import Mock, patch
from MovieData.tmdb_client import TMDbClient

@pytest.fixture
def mock_client():
    return TMDbClient(api_key="test_key")

def test_get_now_playing(mock_client: TMDbClient):
    mock_response = {
        "results": [
            {"id": 1, "title": "Test Movie"},
            {"id": 2, "title": "Another Movie"}
        ]
    }
    
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=Mock()
        )
        
        movies = mock_client.get_now_playing("GR")
        assert len(movies) == 2
        assert movies[0]["title"] == "Test Movie"

def test_get_movie_details(mock_client: TMDbClient):
    mock_response = {
        "id": 123,
        "title": "Inception",
        "credits": {
            "crew": [
                {"id": 1, "job": "Director", "name": "Christopher Nolan"}
            ]
        }
    }
    
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=Mock()
        )
        
        details = mock_client.get_movie_details(123)
        assert details["title"] == "Inception"
        assert len(details["credits"]["crew"]) > 0

def test_error_handling(mock_client: TMDbClient):
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.raise_for_status.side_effect = Exception("API Error")
        
        with pytest.raises(Exception) as excinfo:
            mock_client.get_now_playing()
        assert "API Error" in str(excinfo.value)