from DB_call import get_db
from flask import jsonify,request
from itsdangerous import URLSafeTimedSerializer
import requests
import json
import hashlib
import uuid
salt=uuid.uuid4().hex.encode('utf-8')
secretkey=uuid.uuid4().hex.encode('utf-8')
def users_all():
    db=get_db()
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Users;')
    users=cursor.fetchall()
    user_api=[]
    for i in users:
        user_api.append({"id":i[0],"fname":i[1],"lname":i[2],"email":i[3],"is_admin":i[4],"bio":i[5]})
    return jsonify(user_api)
def user_one(data):
    db=get_db()
    cursor=db.cursor()
    if(isinstance(data,int)):
        cursor.execute("SELECT * FROM Users WHERE personID = %s;",(data,))
    elif(isinstance(data,str)):
        cursor.execute("SELECT * FROM Users WHERE e_mail = %s;",(data,))
    that_user=cursor.fetchone()
    if that_user:
        user_api={that_user[0]:{"first_name":that_user[1],"last_name":that_user[2],"email":that_user[3],"is_admin":that_user[4],"bio":that_user[5]}}
    else:
        return {"error":"Not Found"}, 404
    return jsonify(user_api)
def post_user():
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        post=json.loads(json_data)
        response=insert_one_user(post)
    elif(isinstance(json_data,dict)):
        password=json_data["password"].encode('utf-8')
        password=hashlib.sha256(password + salt).hexdigest()
        json_data["password"]=password
        response=insert_one_user(json_data)
    return(response)
def insert_one_user(data):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE e_mail = %(email)s",data)
    check=cursor.fetchone()
    if(check[0]>0):
        return {"error":"User exists"},409
    cursor.execute("INSERT INTO Users (F_name,L_name,e_mail,is_admin,bio) VALUES (%(fname)s,%(lname)s,%(email)s,%(is_admin)s,%(bio)s)",data)
    cursor.execute("SELECT personID FROM Users WHERE e_mail = %(email)s",data)
    that_user_id=cursor.fetchone()
    hash_pass_dict={
        'password':data['password'],
        'personID':that_user_id[0]
    }
    cursor.execute("INSERT INTO Passes (hash_pass,personID) VALUES (%(password)s,%(personID)s)",hash_pass_dict)
    data.update({"id":that_user_id[0]})
    cursor.close()
    db.commit()
    return data,201


#def auth_check(personID):