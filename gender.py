import requests
from config import tmdb_api_key
import logging

logging.basicConfig(level=logging.ERROR)


def get_crew_genders(imdb_id):
    # This url is formatted to take an IMDB ID from the Bechdel Test API and will not work with generic IMDB numbers.
    movie_url = f'https://api.themoviedb.org/3/find/tt{imdb_id}?external_source=imdb_id&api_key={tmdb_api_key}'

    try:
        movie_response = requests.get(movie_url)
        movie_data = movie_response.json()

        # Check if 'movie_results' key exists
        if 'movie_results' not in movie_data or not movie_data['movie_results']:
            print(f"No movie found with IMDb ID: {imdb_id}")
            return None

        # This returns the TMDB ID number, which we can use to make a separate call with, and get crew information.
        tmdb_movie_id = movie_data['movie_results'][0]['id']

        credits_url = f'https://api.themoviedb.org/3/movie/{tmdb_movie_id}/credits?api_key={tmdb_api_key}'
        credits_response = requests.get(credits_url)
        credits_data = credits_response.json()

        result = []
        for crew_member in credits_data.get('crew', []):
            job = crew_member['job']
            if job == 'Director' or job == 'Original Music Composer' or job == 'Composer':
                gender_id = crew_member['gender']
                name = crew_member['name']

                # TMDB lists gender as follows: 0 = Not set, 1 = Female, 2 = Male, 3 = Non-Binary
                gender = 'Female' if gender_id == 1 else 'Male' if gender_id == 2 else 'Non-Binary' if gender_id == 3 else 'Not specified'

                result.append(f"The {job} of this film is {name}, who identifies as {gender}.")
        if result:
            return "\n".join(result)
        else:
            return "No relevant crew members found."

    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")
        return None
