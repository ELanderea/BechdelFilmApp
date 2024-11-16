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
.
├── app.py                # Main application logic and user interaction
├── bechdel.py            # Handles Bechdel Test checks and film identification
├── config.py             # Configuration for API keys and URLs
├── tmdb_client.py        # Handles interactions with the TMDB API
├── actress.py            # Functions for actress-based movie recommendations
├── genre.py              # Functions for genre-based recommendations
├── year.py               # Year-based movie recommendation logic
├── gender.py             # Functions to get gender details of the film crew
├── display_movie.py      # Displaying detailed movie information
├── random_rec.py         # Fetches random film recommendations
├── tests/
│   ├── test_actress.py   # Tests for actress-based functions
│   ├── test_genre.py     # Tests for genre-based functions
│   ├── test_year.py      # Tests for year-based functions
│   ├── test_random.py    # Tests for random film recommendations
│   └── __init__.py       # Marks the tests directory as a Python package
└── README.md             # Project documentation (this file)
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
  - Enter the film's full title or a keyword. 
  - Confirm your choice from the resulting list of matching films.
  - View the score and decide if you want to see crew gender details.
- Select Options 2-6 to get recommendations of films that completely pass the Bechdel Test.
  (You can search by year or decade, genre, actress, or ask for a random recommendation.
- Select Option 7 to exit the application. 

## Testing Suite
This project includes a comprehensive testing suite to ensure the reliability of its core features. The tests are located in the tests/ directory and cover various aspects of the app's functionality.

### Running Tests
To run the test suite, use the following command:

```bash
Copy code
python -m unittest discover -s tests
```

### Tests Overview
- `test_actress.py`: Tests the actress-based film search and recommendation functions.
- `test_genre.py`: Ensures genre-based recommendations work as expected.
- `test_year.py`: Validates the year-based recommendation logic.
- `test_random.py`: Checks that random film recommendations are properly generated.

### Test Structure and Best Practices
Each test file uses the unittest framework and unittest.mock for mocking API responses and user input to ensure isolation from external dependencies. Tests validate core functionalities, such as:
- Correct film identification and data parsing.
- Handling of missing or partial data.
- User input scenarios and expected outcomes.

### Future Enhancements
- **Graphical User Interface (GUI)**: Develop a more user-friendly interface.
- **TV Series Support**: Extend functionality to include TV series.
- **Additional Filters**: Add filters for runtime, director, and more.


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

Note: By submitting a contribution, you agree to transfer ownership of the contribution to the project owner, ELanderea. This helps maintain a cohesive project and ensures all code aligns with the project’s goals.

## License
This project is proprietary. All rights reserved. Any use, distribution, or modification of the code is not permitted without explicit permission from the owner. For more details or inquiries, please contact ELanderea directly.

## Contact
For any questions or feedback, please contact:
GitHub: ELanderea

