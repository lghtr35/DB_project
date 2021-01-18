from flask import jsonify,request
from API import salt
import requests
import json
import hashlib
import uuid
class User:
    def __init__(self,id=None,email=None,fname=None,lname=None,bio=None,is_admin=None,password=None,confirmed=None):
        self.id=id
        self.email=email
        self.fname=fname
        self.lname=lname
        self.bio=bio
        self.is_admin=is_admin
        self.password=password
        self.confirmed=confirmed
        self.posts={}
class All_users:
    def __init__(self):
        self.all_users=[]
        self.user_count=0
    def get_all_users(self):
        response=requests.get('http://localhost:8080/api/users/all')
        data_dict=json.loads(response.text)
        for i in data_dict:
            a=User(i['id'],i['email'],i['fname'],i['lname'],i['bio'],i['is_admin'],i['confirmed'])
            self.all_users.append(a)
        self.user_count=len(self.all_users)
        return [self.all_users,self.user_count]
    def post_new_user(self,new_user):
        new_user.password=new_user.password.encode('utf-8')
        hash_pass=hashlib.sha256(new_user.password + salt).hexdigest()
        post = {
            'fname':new_user.fname,
            'email':new_user.email,
            'bio':new_user.bio,
            'is_admin':new_user.is_admin,
            'password':hash_pass,
            'lname':new_user.lname
        }
        json_data=json.dumps(post)
        requests.post('http://localhost:8080/api/signup/add_user',json=json_data)
