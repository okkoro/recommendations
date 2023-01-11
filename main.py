from flask import Flask, jsonify
import firebase_admin
from firebase_admin import firestore, credentials
import os

api = Flask(__name__)

db_key_path = os.environ.get("DB_KEY_PATH")

cred = credentials.Certificate(f"{db_key_path}")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
movies_ref = db.collection(u"movies")

# For now, I know id 100 exists so I'll just get that


@api.route("/api/recommendation")
def getMovie():
    ids = ["100", "10023", "10054", "10063", "10069", "10072", "10081", "10105", "101173", "10133"]
    movies = []
    for movieId in ids:
        movies.append(movies_ref.document(movieId).get().to_dict())

    return jsonify(movies), 200
