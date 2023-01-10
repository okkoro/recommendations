import unittest
from dotenv import load_dotenv
import os

path = 'C:\\Users\\cadie\\github\\recommendations'
project_folder = os.path.expanduser(path)  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

from main import api


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.api = api.test_client()


class GetMovieTestCase(BaseCase):
    def test_get_movie(self):
        response = self.api.get("/api/recommendation")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 100)


if __name__ == '__main__':
    unittest.main()
