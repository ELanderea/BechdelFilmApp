import random
from tmdb_client import TMDBClient
from display_movie import Movie
from config import tmdb_api_key


class Genre:
    """Represents a genre and manages its operations"""
    def __init__(self, filmid, name):
        # Initialise a Genre instance with ID and name
        self.id = filmid
        self.name = name

    @staticmethod
    def choose_genre(genres):
        """Allows the user to choose a genre by ID"""
        # Sort the list of genres by their ID
        sorted_genres = sorted(genres, key=lambda x: x['name'])
        print("Available Genres: ")
        # Print the available genres with incrementing numbers
        for index, genre in enumerate(sorted_genres, start=1):
            print(f"{index}: {genre['name']}")

        # Prompt user to input a Genre ID
        try:
            genre_number = int(input("\nPlease select a Genre Number from the list above: ").strip())
            if not (1 <= genre_number <= len(sorted_genres)):
                raise ValueError("Invalid number selected.")

            # Get the selected genre dictionary from the sorted list
            selected_genre_data = sorted_genres[genre_number - 1]
            # Create and return a Genre instance
            selected_genre = Genre(filmid=selected_genre_data['id'], name=selected_genre_data['name'])

            # Return or use the selected genre ID as needed
            print(f"You selected: {selected_genre.name}")
            return selected_genre

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number.")
            return None


class FilmGenreRecommender:
    """Manages the process of recommending movies"""

    def __init__(self, client):
        # Initialise RecommendationSystem with TMDB client
        self.client = client

    def recommend_movies_by_genre(self):
        """Recommends movies based on the users chosen genre"""
        # Fetch list of genres
        genres = self.client.get_genres()
        # Allow the user to choose a genre
        selected_genre = Genre.choose_genre(genres)
        if not selected_genre:
            return  # Exit if the user did not select a valid genre

        genre_movies = []
        # Fetch movies for the selected genre across the first 4 pages
        for page in range(1, 5):
            genre_movies.extend(self.client.discover_movies_by_genre(selected_genre.id, page))

        if genre_movies:
            print("\nPlease wait while we curate your recommendations...\n")
            # Shuffle the list of movies to randomise recommendations
            random.shuffle(genre_movies)

            recommended_movies = []
            # Create Movie instances for valid movies and add them to the recommendations
            for movie_data in genre_movies:
                if len(recommended_movies) >= 5:
                    break  # Limit to 5 recommended movie
                movie = Movie.from_tmdb(movie_data, self.client)
                if movie:
                    recommended_movies.append(movie)

            if recommended_movies:
                # Print the recommended movies
                print(f"\nHere are some '{selected_genre.name}' movies, which pass the Bechdel Test: \n")
                for movie in recommended_movies:
                    movie.display()
            else:
                print(f"No movies from Genre ID {selected_genre.id}: {selected_genre.name}' pass the Bechdel Test")
        else:
            print(f"No movies found for genre ID '{selected_genre.name}'")


if __name__ == "__main__":
    # Create a TMDBClient instance with API key
    tmdb_client = TMDBClient(tmdb_api_key)
    # Create a FilmGenreRecommender instance with TMDBClient
    genre_recommendation = FilmGenreRecommender(tmdb_client)
    # Run the recommendation system to suggest movies based on genre
    genre_recommendation.recommend_movies_by_genre()
