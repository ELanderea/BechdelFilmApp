import unittest
from unittest.mock import patch
from tmdb_client import TMDBClient


class TestTMDBClient(unittest.TestCase):
    def setUp(self):
        self.client = TMDBClient(api_key='dummy_api_key')

    @patch('requests.get')
    def test_get_genres(self, mock_get):
        mock_get.return_value.json.return_value = {'genres': [{'id': 28, 'name': 'Action'}]}
        genres = self.client.get_genres()
        self.assertEqual(len(genres), 1)
        self.assertEqual(genres[0]['name'], 'Action')

    @patch('requests.get')
    def test_discover_movies_by_genre(self, mock_get):
        mock_get.return_value.json.return_value = {'results': [{'title': 'Die Hard'}]}
        movies = self.client.discover_movies_by_genre(28, 1)
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]['title'], 'Die Hard')

    @patch('requests.get')
    def test_get_movie_details(self, mock_get):
        mock_get.return_value.json.return_value = {'title': 'Inception', 'imdb_id': 'tt1375666'}
        details = self.client.get_movie_details(123)
        self.assertEqual(details['title'], 'Inception')


if __name__ == '__main__':
    unittest.main()
