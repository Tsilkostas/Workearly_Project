
import requests
from typing import Dict, List, Optional
from config import API_KEY, API_READ_ACCESS_TOKEN
import os

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

class TMDbClient:
    """Client for interacting with The Movie Database API using Bearer token authentication."""
    
    def __init__(self):
        """Initialize the client with API key and configure authentication headers.
        
        Args:
            api_key: Your TMDb API key (defaults to value from config)
        """
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}",
            "Content-Type": "application/json;charset=utf-8"
        })
        
    def get_now_playing(self, region: str = "GR") -> List[Dict]:
        """Get movies currently playing in theaters in specified region.
        
        Args:
            region: ISO 3166-1 alpha-2 country code (default: "GR" for Greece)
            
        Returns:
            List of movie dictionaries
        """
        url = f"{BASE_URL}/movie/now_playing"
        params = {"region": region}  
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a specific movie.
        
        Args:
            movie_id: TMDb movie ID
            
        Returns:
            Dictionary containing movie details
        """
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {"append_to_response": "credits"}  
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_person_details(self, person_id: int) -> Dict:
        """Get details about a person (director).
        
        Args:
            person_id: TMDb person ID
            
        Returns:
            Dictionary containing person details
        """
        url = f"{BASE_URL}/person/{person_id}"
        response = self.session.get(url) 
        response.raise_for_status()
        return response.json()
    
    def download_poster(self, poster_path: str, save_dir: str = "posters") -> Optional[str]:
        """Download a movie poster and save it locally.
        
        Args:
            poster_path: Relative path from TMDb (e.g., "/kCGlIMHnOm8JPXq3rXMrukC5iTw.jpg")
            save_dir: Directory to save posters (default: "posters")
            
        Returns:
            Local file path if successful, None otherwise.
        """
        if not poster_path:
            return None

        os.makedirs(save_dir, exist_ok=True)
        poster_url = f"{POSTER_BASE_URL}{poster_path}"
        local_path = os.path.join(save_dir, os.path.basename(poster_path))
        
        try:
            response = self.session.get(poster_url)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
        except Exception as e:
            logging.error(f"Failed to download poster: {e}")
            return None