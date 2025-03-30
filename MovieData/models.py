
from dataclasses import dataclass

@dataclass
class Movie:
    tmdb_id: int
    title: str
    original_title: str
    description: str
    release_date: str

@dataclass
class Director:
    tmdb_id: int
    name: str
    imdb_id: str