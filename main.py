from flask import Flask, jsonify
import firebase_admin
from firebase_admin import firestore, credentials
import os

# path = '/home/ClementCadieux/recommendations'
#
# project_folder = os.path.expanduser(path)  # adjust as appropriate
# load_dotenv(os.path.join(project_folder, '.env'))
api = Flask(__name__)

db_key_path = os.environ.get("DB_KEY_PATH")

cred = credentials.Certificate(f"{db_key_path}")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
movies_ref = db.collection(u"movies")

# For now, I know id 100 exists so I'll just get that

@api.route("/api/recommendation")
def getMovie():
    movie = movies_ref.document("100").get()
    print(movie.to_dict())
    return jsonify(movie.to_dict()), 200
