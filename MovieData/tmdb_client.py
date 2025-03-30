
import requests
from typing import Dict, List
from config import API_KEY

BASE_URL = "https://api.themoviedb.org/3"

class TMDbClient:
    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        
    def get_now_playing(self, region: str = "GR") -> List[Dict]:
        """Get movies currently playing in theaters in specified region"""
        url = f"{BASE_URL}/movie/now_playing"
        params = {
            "api_key": self.api_key,
            "region": region
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a specific movie"""
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "append_to_response": "credits"
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_person_details(self, person_id: int) -> Dict:
        """Get details about a person (director)"""
        url = f"{BASE_URL}/person/{person_id}"
        params = {"api_key": self.api_key}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()