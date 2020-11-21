from flask import g
import mysql.connector
def get_db():
    if 'db' not in g:
        g.db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="sanane22021999",
            database="Itu_soc_app"
        )
    return g.db
