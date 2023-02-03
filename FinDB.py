class FinDB:

    def __init__(self, db):
        self.db = db
        self.__cur = db.cursor()

    def get_user(self, user_id):
        query = f"""SELECT * FROM users WHERE id={user_id};"""
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if res:
                return res
        except Exception as ex:
            print(ex)
        return False
