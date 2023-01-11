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
        ids = [100, 10023, 10054, 10063, 10069, 10072, 10081, 10105, 101173, 10133]
        response = self.api.get("/api/recommendation")
        self.assertEqual(response.status_code, 200)
        for i in range(0, len(ids)):
            self.assertEqual(ids[i], response.json[i]['id'])


if __name__ == '__main__':
    unittest.main()
