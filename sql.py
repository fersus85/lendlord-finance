from flask import g
import pymysql
from pymysql import cursors


def connect_db():
    con = pymysql.connect(
            host='185.114.245.124',
            port=3306,
            user='ca56059_finance',
            password='5EdYsVq6',
            database='ca56059_finance',
            cursorclass=cursors.DictCursor
        )
    print('connect')

    return con


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()



# try:
#     con = pymysql.connect(
#         host='185.114.245.124',
#         port=3306,
#         user='ca56059_finance',
#         password='5EdYsVq6',
#         database='ca56059_finance',
#     )
#     print('connect')
#     try:
#         with con.cursor() as cursor:
            # cursor.execute(
            #     """INSERT INTO users(username, hash) VALUES ('dejkgik', 'dsa435dagf98s')"""
            # )
            # con.commit()

            # cursor.execute(
            #     """SELECT * FROM users;"""
            # )
            # rows = cursor.fetchall()
            # print(rows[3][0])

            # cursor.execute(
            #     f"""SELECT * FROM users WHERE username = 'derik';"""
            # )
            # user = cursor.fetchall()
            # print(len(user))
            # if len(user) != 0:
            #     print('no')
            # else:
            #     print('yes')
        # create flash message 'username already exist'

#     finally:
#         con.close()
# except Exception as ex:
#     print(ex)
