import mysql.connector
from mysql.connector import Error
def get_db():
    #db=mysql.connector.connect(
    #        host="us-cdbr-east-03.cleardb.com",
    #        user="b07da6fa923ec8",
    #        password="53618f58",
    #        database="heroku_9d68bac344849a5",
    #        )
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanane22021999",
            database="itu_social_app",
            )  
        return db
    except Error as e:
        print(e)
