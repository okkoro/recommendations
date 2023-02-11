class ReviewRepo:
    shared = None

    def __init__(self, db):
        self.db = db
        self.reviews_ref = db.collection(u"reviews")
        ReviewRepo.shared = self

    @staticmethod
    def getOrCreate(db):
        if ReviewRepo.shared is None:
            return ReviewRepo(db)

        return ReviewRepo.shared

    def getReviews(self, uid):
        reviews = self.reviews_ref.document(uid).get().to_dict()
        return reviews
