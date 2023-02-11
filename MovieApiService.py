import requests


class MovieService:
    shared = None

    def __init__(self, apiLink, apiKey):
        self.apiLink = apiLink
        self.apiKey = apiKey
        MovieService.shared = self

    @staticmethod
    def getOrCreate(apiLink, apiKey):
        if MovieService.shared is None:
            return MovieService(apiLink, apiKey)

        return MovieService.shared

    def getSimilar(self, movie_id):
        response = requests.get(f"{self.apiLink}/movie/{movie_id}/recommendations?api_key={self.apiKey}").json()["results"]

        return response
