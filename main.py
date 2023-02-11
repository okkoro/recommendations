from flask import Flask, jsonify
import firebase_admin
from firebase_admin import firestore, credentials
from UserRepository import UserRepo
import os

api = Flask(__name__)

db_key_path = os.environ.get("DB_KEY_PATH")

cred = credentials.Certificate(f"{db_key_path}")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
userRepo = UserRepo.getOrCreate(db)
movies_ref = db.collection(u"movies")


@api.route("/api/recommendation/<uid>")
def getMovies(uid):
    user = userRepo.getUser(uid)

    bannedIds = set()

    for listedMovie in user["listedMovies"]:
        lists = listedMovie["lists"]

        if "liked" in lists or "watched" in lists:
            bannedIds.add(listedMovie["movieId"])

    movies = movies_ref.stream()

    recomms = []

    for movie in movies:
        movieId = movie.to_dict()['id']

        if movieId not in bannedIds:
            recomms.append(movie.to_dict())

        if len(recomms) >= 10:
            return jsonify(recomms), 200

    return jsonify(recomms), 200
