class MovieRepo:
    shared = None

    def __init__(self, db):
        self.db = db
        self.movies_ref = db.collection(u"movies")
        MovieRepo.shared = self

    @staticmethod
    def getOrCreate(db):
        if MovieRepo.shared is None:
            return MovieRepo(db)

        return MovieRepo.shared

    def getMovie(self, uid):
        movie = self.movies_ref.document(uid).get().to_dict()
        return movie
