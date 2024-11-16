from tmdb_client import TMDBClient
from gender import get_crew_genders
from genre import FilmGenreRecommender
from random_rec import get_random_film
from year import FilmYearRecommender
from config import tmdb_api_key
from actress import search_by_actress
from bechdel import Film


class App:
    """Main application class for managing user interaction and navigating menu options."""

    @staticmethod
    def menu(year_recommendation=None, genre_recommendation=None):
        """Displays the main menu and handles user input for different options."""
        if year_recommendation is None:
            # Instantiate FilmYearRecommender if not provided
            year_recommendation = FilmYearRecommender(TMDBClient(tmdb_api_key))
        if genre_recommendation is None:
            # Instantiate FilmGenreRecommender if not provided
            genre_recommendation = FilmGenreRecommender(TMDBClient(tmdb_api_key))

        while True:
            # Display menu options to the user
            print("1 - Check the Bechdel Test Score of a specific film")
            print("2 - Check whether a film has a female Director or Composer")
            print("3 - Ask for a Film Recommendation based on a specific year")
            print("4 - Ask for a Film Recommendation based on a specific genre")
            print("5 - Ask for a Film Recommendation based on a specific actress")
            print("6 - Get a Film Recommendation at random")
            print("7 - Exit\n")

            try:
                # Get the user's menu choice and validate
                next_step = int(input("Choose between Options 1-7: "))
                if next_step not in range(1, 8):
                    raise ValueError
            except ValueError:
                print("Invalid option, please choose between numbers 1-7.")
                continue  # If invalid option, ask the user to try again

            # Handle the user's choice
            if next_step == 1:
                film = Film.identify()
                Film.gender(film)
            elif next_step == 2:
                film2 = Film.identify()
                print(get_crew_genders(film2.imdb_id))
            elif next_step == 3:
                year_recommendation.recommend_movies_by_year()
            elif next_step == 4:
                genre_recommendation.recommend_movies_by_genre()
            elif next_step == 5:
                search_by_actress()
            elif next_step == 6:
                get_random_film()
            elif next_step == 7:
                print("Exiting the program now. Thanks for using the Bechdel Film App!")
                return


def run():
    # Display welcome message and explanation of the Bechdel Test
    print('#' * 40)
    print('Welcome to the Bechdel Film App!')
    print('#' * 40 + '\n')
    print('The Bechdel Test identifies where films fall on a scale of 0-3 in terms of being feminist.\n')
    print('A film may be regarded as feminist if it satisfies three basic requirements:')
    print('1- The film has at least two female characters.')
    print('2- These two female characters speak to each other.')
    print('3- The conversation is not about a man.\n')

    while True:
        # Display the menu and await user interaction
        App.menu()

        break  # Exit after user chooses to end the session


if __name__ == '__main__':
    run()
