import random
from tmdb_client import TMDBClient
from display_movie import Movie
from config import tmdb_api_key


class FilmYearRecommender:
    """Manages the process of recommending movies based on the user's input"""

    def __init__(self, tmdb_client):
        # Initialise with a TMDBClient instance for API interactions
        self.tmdb_client = tmdb_client

    @staticmethod
    def get_year_filter(year_input):
        """Determine the year filter based on user input"""
        year_input = year_input.strip()

        if year_input.isdigit() and len(year_input) == 4:
            # Handle input as a specific year
            year = int(year_input)
            if year % 10 == 0:
                # If the year is a round decade year (e.g., 2000)
                clarification = input(
                    f"Did you mean '{year}' as a specific year or as the start of the decade '{year}'? "
                    f"Enter 'y' for specific year of 'd' for decade: "
                ).strip().lower()

                if clarification == 'd':
                    # Return filter for the whole decade
                    return f"{year}-01-01,{year + 9}-12-31"
                elif clarification == 'y':
                    # Return filter for the specific year
                    return f"{year}-01-01,{year}-12-31"
                else:
                    print("Invalid input. Please enter 'y' for specific year or 'd' for decade.")
                    return None
            else:
                # Handle input as a specific year
                return f"{year}-01-01,{year}-12-31"

        elif year_input.lower().endswith('s') and len(year_input) in [3, 5]:
            # Handle input as a decade (e.g., '60s', '1980s')
            decade_prefix = year_input[:2] if len(year_input) == 3 else year_input[:4]
            if decade_prefix == "00":
                # Special case for 00s to determine the century
                clarification = input(
                    "Did you mean '2000s' or '1900s'? "
                    "Enter '2' for 2000s or '19' for 1900s: "
                ).strip()
                if clarification == '2':
                    decade = "2000"
                elif clarification == '19':
                    decade = "1900"
                else:
                    print("Invalid input. Please select either '2' or '19' to continue.")
                    return None
            else:
                decade = f"19{decade_prefix}"

            # Return filter for the specified decade
            return f"{decade}-01-01,{int(decade) + 9}-12-31"

        else:
            # Raise an error if the input is invalid
            raise ValueError("Invalid input. Please enter a valid year (2024) or decade (60s, 1980s)")

    def recommend_movies_by_year(self):
        """Recommend movies based on the user's chosen year or decade"""
        while True:
            try:
                # Prompt user to enter a year or decade
                year_input = input("Please enter a specific year or decade (2024, 60s, 80s, 2000s, 1980s): ").strip()
                year_filter = self.get_year_filter(year_input)

                if not year_filter:
                    print("Invalid input. Please try again.")
                    continue

                movies = []
                # Fetch movies for the specified year range across the first 4 pages
                for page in range(1, 5):
                    page_movies = self.tmdb_client.discover_movies_by_year(year_filter, page)
                    movies.extend(page_movies)

                if movies:
                    print("\nPlease wait while we curate your recommendations...\n")
                    # Shuffle the list of movies to randomise recommendations
                    random.shuffle(movies)
                    recommended_movies = []

                    # Create Movie instances for valid movies and add them to the recommendations
                    for movie_data in movies:
                        if len(recommended_movies) >= 5:
                            break  # Limit to 5 recommended movies

                        movie = Movie.from_tmdb(movie_data, self.tmdb_client)
                        if movie:
                            recommended_movies.append(movie)

                    if recommended_movies:
                        print(
                            f"\nHere are some movies from the '{year_input}' year/decade, which pass the Bechdel "
                            f"Test: \n")
                        for movie in recommended_movies:
                            movie.display()
                    else:
                        print(f"No movies released in '{year_input}' pass the Bechdel Test")
                else:
                    print(f"No movies found for the year/decade '{year_input}'")
                break

            except ValueError:
                #  Handle invalid year or decade input
                print("Invalid input. Please enter a valid year or decade.")


if __name__ == "__main__":
    # Create a TMDBClient instance with API key
    tmdb_client_instance = TMDBClient(tmdb_api_key)  # Rename this variable to avoid shadowing
    # Create a FilmRecommender instance with the TMDB client instance
    recommender = FilmYearRecommender(tmdb_client_instance)
    # Run the recommendation process based on year or decade
    recommender.recommend_movies_by_year()
