from unittest import TestCase
from unittest.mock import patch
from year import FilmYearRecommender

class TestFilmYearRecommender(TestCase):
    @patch('builtins.input', side_effect=['y'])
    def test_get_year_filter_specific_year(self, mock_input):
        recommender = FilmYearRecommender(None)  # Passing None as we're only testing the static method
        year_filter = recommender.get_year_filter('2020')
        self.assertEqual(year_filter, '2020-01-01,2020-12-31')

    @patch('builtins.input', side_effect=['d'])
    def test_get_year_filter_decade(self, mock_input):
        recommender = FilmYearRecommender(None)
        year_filter = recommender.get_year_filter('2020')
        self.assertEqual(year_filter, '2020-01-01,2029-12-31')

if __name__ == '__main__':
    import unittest
    unittest.main()
