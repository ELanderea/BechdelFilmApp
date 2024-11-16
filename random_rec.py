import requests
import random
from collections import deque
from itertools import islice
from config import tmdb_api_key


class Movie:
    """Represents a movie and its related data."""
    def __init__(self, title, tmdb_id, imdb_id, synopsis, rating, genre, release_year,
                 bechdel_score, female_actors, film_url):
        # Initialise the Movie object with it's provided attributes
        self.title = title
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id
        self.synopsis = synopsis
        self.rating = rating
        self.genre = genre
        self.release_year = release_year
        self.bechdel_score = bechdel_score
        self.female_actors = female_actors
        self.film_url = film_url

    def __str__(self):
        """Provides a string representation of the movie."""
        # Return the movie details in a readable format
        return (
                f"Title: {self.title}\n"
                f"Bechdel Score: {self.bechdel_score}\n"
                f"Rating: {self.rating:.1f}\n"
                f"Genre: {', '.join(self.genre)}\n"
                f"Release Year: {self.release_year}\n"
                f"Female Actors: {', '.join(self.female_actors)}\n"
                f"URL: {self.film_url}\n"
                f"Synopsis: {self.synopsis}\n"
                + "-" * 60
        )


class GetMovie:
    """Fetches movie data from external APIs."""
    def __init__(self, api_key):
        # Initialise the GetMovie with the TMDB key
        self.api_key = api_key
        self.tmdb_base_url = "https://www.themoviedb.org/movie/"  # Base URL for movie details
        self.bechdel_url = "https://bechdeltest.com/api/v1/getMovieByImdbId"  # Bechdel API URL

    def get_movies(self, pages=5):
        """Fetches a list of movies from TMDB. The number of pages fetched from is determined by the 'pages' parameter
        """

        # Initialise an empty list to store movies
        movies = []

        # Loop through the specified number of pages to gather movies
        for page in range(1, pages + 1):
            # Construct the URL for the API request, using the API key
            discover_url = f"https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&page={page}"

            # Send a GET request to TMDB API and convert the response to JSON format
            response = requests.get(discover_url).json()

            # Extend the movie list with the results from the current page
            movies.extend(response.get('results', []))

        # Shuffle the list of movies to randomise the order
        random.shuffle(movies)

        # Convert the movie list to a deque for efficient popping from the left
        return deque(movies)

    def get_movie_details(self, tmdb_id):
        """Fetches detailed information for a movie from TMDB."""

        # Construct URLs to fetch movie details and credits
        movie_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={self.api_key}"
        movie_credits_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={self.api_key}"

        # send GET requests to TMDB API to get movie details and credits
        details_response = requests.get(movie_details_url).json()
        credits_response = requests.get(movie_credits_url).json()

        # Extract release date and further extract the release year
        release_date = details_response.get('release_date', 'Unknown release date')
        release_year = release_date.split('-')[0] if release_date != 'Unknown release date' else 'Unknown'

        # Extract names of female actors from credits
        female_actors = [
            cast_member['name']
            for cast_member in credits_response.get('cast', [])
            if cast_member['gender'] == 1
        ]

        # Extract genres from the movie details
        genre = [
            genre['name']
            for genre in details_response.get('genres', [])
        ]

        # Return a dictionary containing the movie details, release year, and female actors
        return {
            "details": details_response,
            "release_year": release_year,
            "female_actors": female_actors,
            "genre": genre
        }

    def get_bechdel_score(self, imdb_id):
        """Fetches the Bechdel Test score using IMDb ID."""

        # Clean the IMDB ID by removing the 'tt' prefix
        imdb_id_cleaned = imdb_id[2:]

        # Construct the URL for the Bechdel Test API request using the cleaned IMDB ID
        bechdel_response = requests.get(f"{self.bechdel_url}?imdbid={imdb_id_cleaned}").json()

        # Return the Bechdel score from the response, defaulting to 0 if not found
        return bechdel_response.get('rating', 0)


class RecommendMovie:
    """Recommends movies that pass the Bechdel Test."""

    def __init__(self, get_movie):
        # Initialise the RecommendMovie with a GetMovie object
        self.get_movie = get_movie

    def recommend(self):
        """Finds and returns a movie that passes the Bechdel Test."""

        # Fetch a deque (double-ended queue) of shuffled movies using GetMovie
        movies = self.get_movie.get_movies()

        # Iterate through each movie in the deque
        for movie in islice(movies, len(movies)):
            # Fetch detailed information for the current movie using its TMDB ID
            movie_details = self.get_movie.get_movie_details(movie['id'])

            # Extract TMDB ID from the movie details
            imdb_id = movie_details["details"].get('imdb_id')
            if not imdb_id:
                continue  # If no IMDB ID is available, skip this movie

            # Fetch the Bechdel Test score for the movie using its IMDB ID
            bechdel_score = self.get_movie.get_bechdel_score(imdb_id)
            if bechdel_score >= 3:
                rating = movie_details["details"].get('vote_average', 0)
                formatted_rating = round(float(rating), 1)

                # If the movie passes the Bechdel Test, create and return a Movie object
                return Movie(
                    title=movie['title'],
                    tmdb_id=movie['id'],
                    imdb_id=imdb_id,
                    synopsis=movie_details["details"].get('overview', 'No Synopsis available'),
                    rating=formatted_rating,
                    genre=movie_details["genre"],
                    release_year=movie_details["release_year"],
                    bechdel_score=bechdel_score,
                    female_actors=movie_details["female_actors"],
                    film_url=f"{self.get_movie.tmdb_base_url}{movie['id']}"
                )

        return None  # If no movie passes the Bechdel Test, return None


def get_random_film():
    """Fetches and displays a random film recommendation."""

    # Create instances of GetMovie and RecommendMovie
    movie_fetcher = GetMovie(tmdb_api_key)
    recommender = RecommendMovie(movie_fetcher)

    # Get a recommended movie that passes the Bechdel Test
    recommended_movie = recommender.recommend()

    # Display the recommended movie's details, or indicate that none was found
    if recommended_movie:
        # Print the details of the recommended movie
        print("Here is a random movie which passes the Bechdel Test: ")
        print(recommended_movie)
    else:
        # Print a message if no movie passes the Bechdel Test
        print("No movies that pass the Bechdel Test were found")

