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
        uid = os.environ.get("CLEMENT_USER_ID")
        bannedIds = {150, 10063, 153}

        response = self.api.get("/api/recommendation/" + uid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 10)
        for movie in response.json:
            self.assertNotIn(movie["id"], bannedIds)


if __name__ == '__main__':
    unittest.main()
