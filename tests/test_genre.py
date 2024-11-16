import unittest
from unittest.mock import patch
from genre import Genre, FilmGenreRecommender


class TestGenreFunctions(unittest.TestCase):
    @patch('builtins.input', side_effect=['1'])
    def test_choose_genre(self, mock_input):
        genres = [{'id': 28, 'name': 'Action'}]
        selected = Genre.choose_genre(genres)
        self.assertIsNotNone(selected)
        self.assertEqual(selected.name, 'Action')


if __name__ == '__main__':
    unittest.main()
