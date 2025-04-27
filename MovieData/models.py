
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Movie:
    tmdb_id: int
    title: str
    original_title: str
    description: str
    release_date: str
    poster_path: Optional[str] = None 
    popularity: Optional[float] = None
    genres: Optional[List[str]] = None

@dataclass
class Director:
    tmdb_id: int
    name: str
    imdb_id: str