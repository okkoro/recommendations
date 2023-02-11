from flask import Flask, jsonify
import firebase_admin
from firebase_admin import firestore, credentials
from UserRepository import UserRepo
from MovieRepository import MovieRepo
from ReviewRepository import ReviewRepo
from MovieApiService import MovieService

import os

api = Flask(__name__)

db_key_path = os.environ.get("DB_KEY_PATH")
api_link = os.environ.get("API_LINK")
api_key = os.environ.get("API_KEY")

cred = credentials.Certificate(f"{db_key_path}")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
userRepo = UserRepo.getOrCreate(db)
movieRepo = MovieRepo.getOrCreate(db)
reviewRepo = ReviewRepo.getOrCreate(db)
movieService = MovieService.getOrCreate(api_link, api_key)


@api.route("/api/recommendation/<uid>")
def getMovies(uid):
    user = userRepo.getUser(uid)

    bannedIds = set()

    for listedMovie in user["listedMovies"]:
        lists = listedMovie["lists"]

        if "liked" in lists or "watched" in lists:
            bannedIds.add(listedMovie["movieId"])

    reviews = reviewRepo.getReviews(user["username"])

    recomms = {}
    received = {}

    for review in reviews:
        reviewDict = review.to_dict()
        score = reviewDict["score"]
        movieId = reviewDict["movieId"]

        similarMovies = movieService.getSimilar(movieId)
        for similar in similarMovies:
            similarId = similar["id"]

            received[similarId] = similar

            oldScore = 0
            oldCount = 0

            if similarId in recomms.keys():
                oldScore = recomms[similarId][0]
                oldCount = recomms[similarId][1]

            newScore = oldScore + (score - oldScore)/(oldCount + 1)
            recomms[similarId] = [newScore, oldCount + 1]

    sortedRecomms = sorted(recomms.items(), key=lambda x: x[1][0])
    result = []

    for recom in sortedRecomms:
        recomId = recom[0]

        if recomId not in bannedIds:
            # try:
            #     movie = movieRepo.getMovie(recomId)
            #     result.append(movie)
            # except Exception:
            #     print(f"Movie {recomId} not in db")
            result.append(received[recomId])

        if len(result) >= 10:
            return jsonify(result), 200

    return jsonify(result), 200
