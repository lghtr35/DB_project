from DB_call import get_db
from flask import jsonify
import requests
class Posts:
    def __init__(self,post_data,author_name,pub_date,personID):
        self.post_data=post_data
        self.author_name=author_name
        self.pub_date=pub_date
        self.personID=personID
#def Posts_all():
#    db=get_db()
    