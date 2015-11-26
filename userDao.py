import md5

class UserDao(object):
    def __init__(self, database):
        self.db = database
        self.user = database.user

    def getUsername(self, username, password):
        m = md5.new()
        m.update(password)
        print "password: md5: ", m.hexdigest()
        result = self.user.find({"username": username, "password": m.hexdigest()})

        for r in result:
            return username

        return None
        