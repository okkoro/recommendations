class UserRepo:
    shared = None

    def __init__(self, db):
        self.db = db
        self.users_ref = self.db.collection(u"users")
        UserRepo.shared = self

    @staticmethod
    def getOrCreate(db):
        if UserRepo.shared is None:
            return UserRepo(db)

        return UserRepo.shared

    def getUser(self, uid):
        user = self.users_ref.document(uid).get().to_dict()
        return user
