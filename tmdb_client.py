import requests


class TMDBClient:
    """Handles communication with the TMDB API."""

    def __init__(self, api_key):
        # Initialise TMDBClient with the API key and set up the base URLs for API requests
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"  # Base URL for TMDB API
        self.bechdel_url = "https://bechdeltest.com/api/v1/getMovieByImdbId"  # URL for Bechdel Test API
        self.tmdb_base_url = "https://www.themoviedb.org/movie/"  # Base URL for movie pages on TMDB

    def get_genres(self):
        """Fetches a list of genres from TMDB and their IDs."""
        # Construct the URL to fetch genre list from TMDB
        url = f"{self.base_url}/genre/movie/list?api_key={self.api_key}"
        response = requests.get(url).json()
        return response['genres']

    def discover_movies_by_genre(self, genre_id, page):
        """Fetches movies from TMDB using a genre ID."""
        # Construct the URL to fetch movies by genre from TMDB
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}&with_genres={genre_id}&page={page}"
        response = requests.get(url).json()
        return response.get('results', [])

    def discover_movies_by_year(self, year_filter, page):
        """Fetches movies from TMDB based on a year range."""
        # Split the year_filter to get start and end years
        start_year, end_year = year_filter.split(',')
        # Construct the URL to fetch movies by year range from TMDB
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}" \
              f"&primary_release_date.gte={start_year}" \
              f"&primary_release_date.lte={end_year}" \
              f"&page={page}"
        response = requests.get(url).json()
        return response.get('results', [])

    def get_movie_details(self, tmdb_id):
        """Fetches detailed information about a movie from TMDB."""
        # Construct the URL to fetch detailed movie information from TMDB
        url = f"{self.base_url}/movie/{tmdb_id}?api_key={self.api_key}&append_to_response=credits"
        response = requests.get(url).json()
        return response

    def get_bechdel_score(self, imdb_id):
        """Fetches Bechdel Test score for a movie using its IMDb ID."""
        imdb_id_cleaned = imdb_id[2:]  # Remove 'tt' prefix
        # Construct the URL to fetch Bechdel test score from the Bechdel Test API
        url = f"{self.bechdel_url}?imdbid={imdb_id_cleaned}"
        response = requests.get(url).json()
        return response.get('rating', 0)

    @staticmethod
    def get_female_actors(film_credits):
        """Extracts female actors from the movie credits."""
        female_actors = []  # Initialise an empty list to store female actors' names
        for actor in film_credits['cast']:
            if actor['gender'] == 1:  # Gender 1 represents female actors in TMDB
                female_actors.append(actor['name'])
        return female_actors
