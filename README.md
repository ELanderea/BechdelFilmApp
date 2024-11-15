# Bechdel Film App

## Overview
The Bechdel Film App is a comprehensive tool designed to interact with The Movie Database (TMDB) and the Bechdel Test API to provide users with film information, recommendations, and insights into gender representation in film. The application includes various features such as checking the Bechdel Test score, identifying female directors or composers, and recommending movies based on different criteria such as year, genre, or starring actresses.

## Features
- **Bechdel Test Score Checker**: Check if a movie passes the Bechdel Test (scoring from 0 to 3).
- **Crew Gender Information**: Identify whether the director or composer of a film is female, male, or non-binary.
- **Year-Based Recommendations**: Get movie recommendations for a specific year or decade.
- **Genre-Based Recommendations**: Choose a movie genre and get recommendations.
- **Actress-Based Recommendations**: Search for movies featuring a specific actress.
- **Random Recommendations**: Get a random movie recommendation that passes the Bechdel Test.

## Project Structure
```tree
├── app.py           # Main application entry point
├── bechdel.py       # Handles interaction with the Bechdel Test API and film selection
├── config.py        # Configuration file containing API keys and URLs
├── tmdb_client.py   # Handles communication with the TMDB API
├── actress.py       # Functions for searching and recommending movies by actresses
├── genre.py         # Classes and functions for genre-based movie recommendations
├── year.py          # Classes for year-based movie recommendations
├── gender.py        # Function to get gender details of the crew
├── display_movie.py # Class for displaying detailed movie information
├── random_rec.py    # Class and function for fetching random movie recommendations
└── tests.py         # Unit tests for various functions
```

## Setup and Installation

### Prerequisites
- Python 3.x
- `requests` library
- API key for TMDB (The Movie Database)

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/bechdel-film-app.git
    cd bechdel-film-app
    ```

2. Install dependencies: Ensure `requests` library is installed:
    ```bash
    pip install requests
    ```

3. Add your TMDB API Key: Replace the placeholder in `config.py` with your own TMDB API key:
    ```python
    tmdb_api_key = 'your_tmdb_api_key'
    ```

## Running the App
To run the application, execute:
```bash
python app.py
```

## Usage
### Main Menu
Upon running the app, you will be presented with a menu:

- Check the Bechdel Test Score of a specific film.
- Check if a film has a female Director or Composer.
- Get movie recommendations by year or decade.
- Get movie recommendations by genre.
- Get movie recommendations featuring a specific actress.
- Receive a random movie recommendation.
- Exit the application.

### Example Workflow
- Select Option 1 to check the Bechdel Test score:
  - Enter the film's title.
  - Choose from the list of matching films.
  - View the score and decide if you want to see crew gender details.
- Select Option 4 to get genre-based recommendations:
  - Choose a genre by number from the displayed list.
  - View up to 5 recommended movies that pass the Bechdel Test.

### Testing
To run unit tests:

```bash
Copy code
python tests.py
```

## Project Highlights
- Caching and Performance: Uses functools.lru_cache to cache frequently requested data, improving performance.
- Threading: Utilizes ThreadPoolExecutor for concurrent Bechdel Test checks to speed up actress-based film searches.
- API Integration: Combines TMDB and Bechdel Test APIs for comprehensive film data.

## Future Enhancements
- Add a graphical user interface (GUI) for a more user-friendly experience.
- Implement additional filters, such as runtime and director-specific searches.
- Extend the app to support TV series in addition to movies.

## Contributions
Contributions to this project are welcome but must be approved by the owner. To contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request for review.

Note: By submitting a contribution, you agree to transfer ownership of the contribution to the project owner, [Your Name]. This helps maintain a cohesive project and ensures all code aligns with the project’s goals.

## License
This project is proprietary. All rights reserved. Any use, distribution, or modification of the code is not permitted without explicit permission from the owner. For more details or inquiries, please contact ELanderea directly.

## Contact
For any questions or feedback, please contact:
GitHub: ELanderea

