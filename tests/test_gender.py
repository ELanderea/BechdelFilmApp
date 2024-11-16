from unittest import TestCase, main
from unittest.mock import patch, Mock
from gender import get_crew_genders
import requests
import logging


class TestGetCrewMembers(TestCase):
    """Unit tests for the get_crew_genders function."""

    def setUp(self):
        """Set up reusable data for tests."""
        self.valid_imdb_id = '1517268'
        self.no_crew_imdb_id = '0000000'
        self.api_failure_id = '9999999'

    @patch('requests.get')
    def test_valid_movie_with_crew(self, mock_get):
        """Test a valid IMDb ID with directors and composers."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'movie_results': [{'id': 123}],
            'crew': [
                {'job': 'Director', 'name': 'Greta Gerwig', 'gender': 1},
                {'job': 'Original Music Composer', 'name': 'Mark Ronson', 'gender': 2}
            ]
        }
        mock_get.return_value = mock_response

        expected = (
            "The Director of this film is Greta Gerwig, who identifies as Female.\n"
            "The Original Music Composer of this film is Mark Ronson, who identifies as Male."
        )
        result = get_crew_genders(self.valid_imdb_id)
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_no_crew_found(self, mock_get):
        """Test a valid IMDb ID with no relevant crew found."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'movie_results': [{'id': 123}],
            'crew': []
        }
        mock_get.return_value = mock_response

        result = get_crew_genders(self.no_crew_imdb_id)
        self.assertEqual(result, "No relevant crew members found.")

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        # Temporarily set the logging level to CRITICAL to suppress error logs
        logging.getLogger().setLevel(logging.CRITICAL)

        mock_get.side_effect = requests.exceptions.RequestException("API call failed")
        result = get_crew_genders('1517268')
        self.assertIsNone(result)

        # Reset the logging level back to default
        logging.getLogger().setLevel(logging.ERROR)

    @patch('requests.get')
    def test_non_binary_crew_member(self, mock_get):
        """Test handling of non-binary crew members."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'movie_results': [{'id': 123}],
            'crew': [
                {'job': 'Director', 'name': 'Alex Smith', 'gender': 3}
            ]
        }
        mock_get.return_value = mock_response

        expected = "The Director of this film is Alex Smith, who identifies as Non-Binary."
        result = get_crew_genders(self.valid_imdb_id)
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_crew_with_unspecified_gender(self, mock_get):
        """Test handling of crew members with unspecified gender."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'movie_results': [{'id': 123}],
            'crew': [
                {'job': 'Composer', 'name': 'Chris Doe', 'gender': 0}
            ]
        }
        mock_get.return_value = mock_response

        expected = "The Composer of this film is Chris Doe, who identifies as Not specified."
        result = get_crew_genders(self.valid_imdb_id)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    main()
