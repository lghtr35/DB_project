import mysql.connector
def get_db():
    
    #db=mysql.connector.connect(
    #        host="us-cdbr-east-03.cleardb.com",
    #        user="b07da6fa923ec8",
    #        password="53618f58",
    #        database="heroku_9d68bac344849a5",
    #        )
    db=mysql.connector.connect(
            host="localhost",
            user="sckmk",
            password="sanane22021999",
            database="itu_social_app",
            )  
    return db
