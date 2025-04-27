
from tmdb_client import TMDbClient
from database import Database
from models import Movie, Director
import logging

class MovieDataApp:
    def __init__(self):
        self.tmdb = TMDbClient()
        self.db = Database()
    
    def fetch_and_store_movie_data(self):
        """Main workflow: fetch data from API and store in database"""
        # Get movies currently playing in Greece
        movies = self.tmdb.get_now_playing("GR")
        
        for movie_data in movies:
            # Get full movie details including credits
            full_movie = self.tmdb.get_movie_details(movie_data["id"])
            
            # Create Movie object
            movie = Movie(
                tmdb_id=full_movie["id"],
                title=full_movie["title"],
                original_title=full_movie["original_title"],
                description=full_movie["overview"],
                release_date=full_movie["release_date"]
            )
            
            # Store movie in database
            movie_id = self.db.upsert_movie(movie)
            
            # Find directors (people with job="Director" in credits)
            directors = [
                person for person in full_movie["credits"]["crew"]
                if person["job"] == "Director"
            ]
            # Download poster if available
            if movie_data.get("poster_path"):
                poster_path = self.tmdb.download_poster(movie_data["poster_path"])
                if poster_path:
                    logging.info(f"Downloaded poster for {movie.title}: {poster_path}")
            
            for director_data in directors:
                # Get director details
                director_info = self.tmdb.get_person_details(director_data["id"])
                
                # Create Director object
                director = Director(
                    tmdb_id=director_info["id"],
                    name=director_info["name"],
                    imdb_id=director_info["imdb_id"]
                )
                
                # Store director in database
                director_id = self.db.upsert_director(director)
                
                # Link movie and director
                self.db.link_movie_director(movie_id, director_id)
                