from flask import g
import mysql.connector
def get_db():
    if 'db' not in g:
        g.db=mysql.connector.connect(
            host="us-cdbr-east-03.cleardb.com",
            user="b07da6fa923ec8",
            password="53618f58",
            database="heroku_9d68bac344849a5"
        )
    return g.db
