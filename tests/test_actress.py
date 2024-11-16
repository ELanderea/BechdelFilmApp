from unittest import TestCase
from unittest.mock import patch
from actress import get_actress_matches

class TestActress(TestCase):
    @patch('actress.requests.get')
    def test_get_actress_matches(self, mock_get):
        mock_response = {
            'results': [
                {
                    'name': 'Meryl Streep',
                    'known_for_department': 'Acting',
                    'gender': 1,
                    'known_for': [{'title': 'The Post'}, {'title': 'Mamma Mia!'}]
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        matches = get_actress_matches('Meryl')
        self.assertTrue(len(matches) > 0)
        self.assertEqual(matches[0]['name'], 'Meryl Streep')
