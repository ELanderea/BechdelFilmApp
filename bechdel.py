import requests
import html
from gender import get_crew_genders


# The BechdelAPI class handles API requests to the Bechdel Test database.
# It includes methods for getting films by title as well as getting film details using IMDB IDs
class BechdelAPI:
    """Handles API requests to the Bechdel Test database for retrieving film data."""

    # Base URL for the Bechdel Test API
    BASE_URL = 'http://bechdeltest.com/api/v1/'

    # Static method to get films by title from the Bechdel API
    @staticmethod
    def get_films(title):
        """Fetches films from the Bechdel API based on a given title."""
        response = requests.get(f'{BechdelAPI.BASE_URL}getMoviesByTitle?title={title}',
                                headers={'content-type': 'application/json'})
        if response.status_code == 200:
            return response.json()

    # Static method to get film details by IMDB IDs from the Bechdel API
    @staticmethod
    def get_title(imdb_id):
        """Fetches film details from the Bechdel API using an IMDb ID."""
        response = requests.get(f'{BechdelAPI.BASE_URL}getMovieByImdbId?imdbid={imdb_id}',
                                headers={'content-type': 'application/json'})
        if response.status_code == 200:
            return response.json()


# The Film class represents a film, including its attributes.
# It also includes methods to fix the films title format and to display the Bechdel score.
class Film:
    """Represents a film, handles Bechdel score display, and user interaction for film selection."""
    def __init__(self, title, year, score, dubious, imdb_id):
        # Initialise a Film object with essential attributes
        self.title = self.fix_film_title(html.unescape(title))  # Fix the film title formatting
        self.year = year
        self.score = score
        self.dubious = dubious
        self.imdb_id = imdb_id

    @staticmethod
    def fix_film_title(title):
        """Formats film titles, e.g., 'Matrix, The' -> 'The Matrix'."""
        words = ["The", "A", "An"]
        sections = title.rsplit(',', 1)  # Split the title at the last comma
        if len(sections) == 2:
            section_1 = sections[0].strip()
            section_2 = sections[1].strip()
            if section_2 in words:
                return f'{section_2} {section_1}'
        return title

    # Method to display the film's Bechdel score and an explanation of what it means
    def display_score(self):
        """Displays the film's Bechdel score with an explanation."""
        print(f'{self.title} ({self.year}) has a score of {self.score}.')
        if self.score == 0:
            print('This means that the film has failed to pass any of the Bechdel Test criteria.')
            print('The most basic element of the Bechdel Test requires at least two named female characters to be '
                  'present.')
        elif self.score == 1:
            print('This means that the film has met the most basic criteria of the Bechdel Test and contains at least '
                  'two named female characters.')
        elif self.score == 2:
            print('This means that two named female characters speak to each other.')
            print('This conversation may have been very brief, or the topic may have been about a male character.')
        elif self.score == 3:
            print('This means that it has successfully passed the Bechdel Test!')
            print('The film contains at least two named female characters, who spend time discussing something other '
                  'than a male character.')
        else:
            print('Error: Unexpected score value.')

        if self.dubious == 1:
            print("Please Note: This score's reliability is marked as dubious and has yet to be verified.")

    @staticmethod
    def identify():
        """Guides the user to select a film based on title input and retrieves the film details."""
        while True:
            # Ask the user to input a film title
            title = input('Please input the title of the film that you would like to check: ')

            if not title:
                print("\nInvalid input. Please try to search for a different keyword.\n")
                continue  # If input is empty ask the user to try again

            # Get film options based on the title input
            film_options = BechdelAPI.get_films(title)
            if not film_options:
                print("\nNo films were found with that title. Please try to search for a different keyword.\n")
                continue  # If no films were found, ask the user to try again

            # Display the list of films that match the search
            print('Here are the titles that match your search: ')
            for idx, film in enumerate(film_options, start=1):
                film_title = Film.fix_film_title(html.unescape(film['title']))
                print(f"Option {idx}: {film_title}, ({film['year']})")

            try:
                # Ask the user to select an option
                selected_option = int(input('Please select which option you wish to check (e.g. "1"): '))
                if not (1 <= selected_option <= len(film_options)):
                    raise ValueError
            except ValueError:
                print("Invalid option selected, please try again.")
                continue  # If invalid option, ask the user to search again

            # Get the selected film's details
            confirmed_film = film_options[selected_option - 1]
            film = Film(confirmed_film['title'], confirmed_film['year'],
                        confirmed_film['rating'], confirmed_film['dubious'],
                        confirmed_film['imdbid'])

            film.display_score()
            return film


    @staticmethod
    def display(film):
        """Displays the selected film's Bechdel score."""
        print(film.display_score())

    @staticmethod
    def gender(film):
        """Displays gender information for the film's crew. """
        while True:
            print('Would you like to also see the gender of the Director and/or Composer for this film? ')
            gender = input('Please indicate either y/n: ').strip().lower()

            if not gender or gender not in ('y', 'n'):
                print("\nInvalid input. Please enter either 'y' or 'n'.\n")
                continue  # If input is invalid, ask the user to try again

            if gender == 'y':
                print(get_crew_genders(film.imdb_id))
                print('\n')
                print('Choose between Options 1-7: ')
                print('\n')

                break

            if gender == 'n':
                print('\n')
                print('Choose between Options 1-7: ')
                print('\n')
                break  # Exit the loop when the user selects 'N'
