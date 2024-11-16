class Movie:
    """Represents a movie and manages its related operations."""

    def __init__(self, title, tmdb_id, bechdel_score, rating, film_url, synopsis, release_year, female_actors):
        # Initialise a Movie instance with the given attributes
        self.title = title
        self.tmdb_id = tmdb_id
        self.bechdel_score = bechdel_score
        self.rating = rating
        self.film_url = film_url
        self.synopsis = synopsis
        self.release_year = release_year
        self.female_actors = female_actors

    @classmethod
    def from_tmdb(cls, movie_data, tmdb_client):
        """Creates a Movie instance using TMDB data."""
        # Extract basic information from the movie_data dictionary
        movie_title = movie_data['title']
        tmdb_id = movie_data['id']

        # Fetch detailed information about the movie using the TMDB client
        details = tmdb_client.get_movie_details(tmdb_id)
        imdb_id = details.get('imdb_id')
        synopsis = details.get('overview', 'No synopsis available')
        rating = details.get('vote_average', 'No rating available')
        film_url = f"{tmdb_client.tmdb_base_url}{tmdb_id}"  # Construct the URL for the movie's page

        # Extract the release year from release_date
        release_year = details.get('release_date', 'N/A')[:4]

        # Extract the female actors from the movie credits
        female_actors = tmdb_client.get_female_actors(details['credits'])

        if imdb_id:
            # Get the Bechdel test score using the IMDB ID
            bechdel_score = tmdb_client.get_bechdel_score(imdb_id)
            if bechdel_score >= 3:
                # Format the rating to one decimal place
                formatted_rating = f"{float(rating):.1f}" if rating != 'No rating available' else rating

                # Return a Movie instance with the gathered data
                return cls(
                    title=movie_title,
                    tmdb_id=tmdb_id,
                    bechdel_score=bechdel_score,
                    rating=formatted_rating,
                    film_url=film_url,
                    synopsis=synopsis,
                    release_year=release_year,
                    female_actors=female_actors
                )
        # Return None if the Bechdel score is less than 3 or if IMDb ID is not available
        return None

    def display(self):
        """Displays movie details."""
        # Create a string listing female actors or a default message if none are listed
        female_actors_str = ', '.join(self.female_actors) if self.female_actors else 'No female actors listed'

        # Format and print the movie details
        movie_details = (
            f"Title: {self.title}\n"
            f"Release Year: {self.release_year}\n"
            f"Bechdel Score: {self.bechdel_score}\n"
            f"Rating: {self.rating}\n"
            f"URL: {self.film_url}\n"
            f"Synopsis: {self.synopsis}\n"
            f"Female Actors: {female_actors_str}\n"
            + "-" * 60  # Separator line for readability
        )
        print(movie_details)   # Output the movie details to the console