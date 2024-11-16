import requests
import random
from config import tmdb_api_key, tmdb_base_url, bechdel_url

# Imports ThreadPoolExecutor for parallel execution of tasks
from concurrent.futures import ThreadPoolExecutor, as_completed
# as_completed is used to handle and process each result as soon as it is available
from functools import lru_cache


# Imports lru_cache for caching function results.
# This stores results of frequently called functions.
# When this same argument is called again, it can return the cached result instead of recalculating/fetching the result.


@lru_cache(maxsize=100)  # maxsize=100 means the cache can store up to 100 different results, once it reaches this
# limit it will discard the least recently used result in order to make room for new ones.
def get_actress_matches(actress_name):
    """Fetches a list of actresses based on a search query."""
    search_url = f"https://api.themoviedb.org/3/search/person?api_key={tmdb_api_key}&query={actress_name}"
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        raise ValueError("Failed to fetch Actresses.")

    # Parse the JSON response
    search_data = search_response.json()
    # Extract the list of actors from the response
    actresses = search_data.get('results', [])
    # Filter the list to include only actors who are in the "Acting" department and are female
    filtered_actresses = [actress for actress in actresses if
                          actress.get('known_for_department') == "Acting" and
                          actress.get('gender') == 1]
    return filtered_actresses


def select_actress(actresses):
    """Displays a list of actresses and allows the user to select one."""
    if not actresses:
        print("No Actresses found.")
        return None  # Return None if no actresses were found

    print(f"\nMultiple Actresses found. Please select your choice from the list below.\n")
    for idx, actress in enumerate(actresses, start=1):
        known_for = actress.get('known_for', [])
        # Filter out 'N/A' and collect up to '3' known films for the actress
        films = [film.get('title', "N/A") for film in known_for if film.get('title', "N/A") != "N/A"][:3]
        films_list = ', '.join(films) if films else "N/A"
        # print each actress with known films
        print(f"{idx}: {actress['name']} - Known For Films like: ({films_list})")

    while True:
        try:
            # Prompt the user to select an actress by entering the corresponding number
            actress_choice = int(input("\nPlease enter the number which matches your actress choice: "))
            if 1 <= actress_choice <= len(actresses):
                selected_actress = actresses[actress_choice - 1]
                return selected_actress['id'], selected_actress['name']  # Return the selected actress's ID and name
            else:
                print(f"Please enter a number between 1 and {len(actresses)}")
        except ValueError:
            print("Invalid Input. Please enter a number.")


def get_movies_with_actress(actor_id):
    """Fetches a list of movies featuring the selected actress."""
    films = []  # Initialise and empty list to store movies
    for page in range(1, 5):  # Fetch up to 4 pages of results
        credits_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?" \
                      f"api_key={tmdb_api_key}&page={page}"
        credits_response = requests.get(credits_url)

        if credits_response.status_code != 200:
            raise ValueError("Failed to fetch movie credits.")

        credits_data = credits_response.json()
        # Add the list of films to the films list
        films.extend(credits_data.get('cast', []))

        if credits_data.get('total_pages', 0) <= page:
            break  # Exit the loop if all pages have been fetched
    return films  # Return the list of films


def check_bechdel(film_id):
    """Checks the Bechdel Test score of a film using its IMDb ID."""
    film_details_url = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={tmdb_api_key}"
    film_details_response = requests.get(film_details_url)

    if film_details_response.status_code != 200:
        raise ValueError("Failed to fetch film details.")

    film_details = film_details_response.json()
    imdb_id = film_details.get('imdb_id')

    if imdb_id:
        imdb_id_cleaned = imdb_id[2:]  # Remove the 'tt' prefix from the IMDB ID
        # Query the Bechdel Test API with the cleaned IMDB ID
        bechdel_response = requests.get(f"{bechdel_url}?imdbid={imdb_id_cleaned}")

        if bechdel_response.status_code != 200:
            raise ValueError("Failed to check Bechdel test.")

        # Parse the Bechdel Test API response and return True if the Bechdel Test rating is 3 or higher
        bechdel_result = bechdel_response.json().get('rating', 0)
        if bechdel_result is None:
            raise ValueError(f"No Bechdel Test rating found for imdb_id: {imdb_id_cleaned}")
        return bechdel_result
    return 0  # Return nothing if there's no IMDb ID


def display_recs(rec_films):
    """Displays recommended films that pass the Bechdel Test."""
    if rec_films:
        print("Recommended films featuring your chosen actress that also pass the Bechdel Test: ")
        for film in rec_films:
            bechdel_score = film.get('bechdel_score', 'Not available')
            rating = film.get('vote_average', 'No rating available')

            # Format and print the details of each recommended film
            film_details = (
                    f"Title: {film['title']}\n"
                    f"Bechdel Score: {bechdel_score}\n"  # Add the bechdel score
                    f"Rating: {rating:.1f}\n"  # Format the rating to .1f
                    f"Synopsis: {film.get('overview', 'No synopsis available')}\n"
                    f"URL: {tmdb_base_url}{film['id']}\n"
                    + "-" * 60
            )
            print(film_details)
    else:
        print("No films featuring this actress pass the Bechdel Test.")


def search_by_actress():
    """Allows users to search for and get movie recommendations based on an actress."""
    while True:
        # Prompt the user to enter the name of an actress or exit the program
        actress_name = input("Enter the first or last name of the actress (or type 'exit' to quit): ").strip()

        if actress_name.lower() == 'exit':
            print("Exiting the program.")
            break  # Exit the main loop and the program

        try:
            actresses = get_actress_matches(actress_name)
        except ValueError:
            print("Failed to retrieve Actress matches.")
            continue  # Continue the loop if there's an error fetching actresses

        if not actresses:
            print("No actresses found. Please try again.")
            continue  # Continue the loop if no actresses are found

        while True:
            if len(actresses) > 1:
                actor_id, actor_full_name = select_actress(actresses)  # Get both ID and full name
            else:
                selected_actress = actresses[0]
                actor_id, actor_full_name = selected_actress['id'], selected_actress['name']

            print(f"\nSearching for movies by '{actor_full_name}'...\n")  # Print the actress's full name

            try:
                films = get_movies_with_actress(actor_id)
            except ValueError:
                print("Error fetching movie credits.")
                break  # Break out of the loop if there's an error fetching movies

            if not films:
                print("No movies found for this actress.")
                break  # Break out of the loop if no movies are found

            # Use ThreadPoolExecutor to check Bechdel Test for each movie concurrently
            with ThreadPoolExecutor(max_workers=5) as executor:  # max_workers=5 can run up to 5 threads in parallel
                # to each other. The with statement ensures that the executor is properly cleaned up after the tasks
                # are completed.
                futures = {executor.submit(check_bechdel, film['id']): film for film in films}
                # futures : Creates a dictionary where each key is a `Future` object and each value is the corresponding
                # `film`. Each `future` represents a task.
                # executor.submit() : The task being submitted is `check_bechdel`, and `film['id']`
                # is passed as an argument to this function.

                # Initialise an empty list to store films that pass the bechdel test
                bechdel_passed_films = []

                # Iterate over the futures as they're completed
                # as_completed returns an iterator that yields futures as they complete
                for future in as_completed(futures):
                    # Retrieve the film associated with the completed future
                    film = futures[future]
                    try:
                        # Get the result from the future, which is the Bechdel score
                        score = future.result()
                        # If the Bechdel score is 3, add the film to the list of passed films
                        if score >= 3:
                            # Add films details and the Bechdel score to the list
                            bechdel_passed_films.append({**film, 'bechdel_score': score})
                    except ValueError:
                        # Suppress specific errors in this context
                        # When testing it was printing out that some films without IMDB IDs were getting passed over
                        # Didn't want this being printed out to the user.
                        pass

            if bechdel_passed_films:
                random.shuffle(bechdel_passed_films)  # Shuffle the list of movies to randomize recommendations
                recommended_films = bechdel_passed_films[:5]  # Select the top 5 movies
                display_recs(recommended_films)  # Display the recommended movies

                print("Exiting the actress search.")
                return  # Exit the main function after successful recommendations
            else:
                print("No Films featuring this Actress pass the Bechdel Test.")
                while True:
                    # Prompt the user to choose another option, displaying options like a dictionary
                    choice = input(
                        "Choose an option from the following:\n"
                        "\n"
                        "  1: 'Choose another actress from the list',\n"
                        "  2: 'Search for a new name',\n"
                        "  3: 'Exit'\n"
                        "\n"
                        "Enter 1, 2, or 3: "
                    ).strip()
                    if choice == '1':
                        break  # Restart the search with the current list of actresses
                    elif choice == '2':
                        break  # Exit the inner loop to restart the entire process with a new name
                    elif choice == '3':
                        print("Exiting the actress search.")
                        return  # Exit the main function
                    else:
                        print("Invalid input. Please enter 1, 2, or 3.")

            if choice == '2':  # Restart the entire process if the user chose to search for a new name
                break


if __name__ == "__main__":
    search_by_actress()
