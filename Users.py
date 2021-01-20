from DB_call import get_db
from flask import jsonify,request
from flask_login import UserMixin
import requests
import json

class User(UserMixin): #login object
    def __init__(self,id,is_admin,email,password,bio=None,fname=None,lname=None):
        self.email = email
        self.password = password
        self.id=id
        self.bio=bio
        self.fname=fname
        self.lname=lname
        self.active = True
        self.is_admin = is_admin
    @property
    def is_active(self):
        return self.active
def get_User_obj(data): #login object getter
    response=requests.get(request.host_url+"/api/users/"+str(data))
    user=json.loads(response.text)
    print(user)
    if "error" not in user:
        response=requests.get(request.host_url+"/api/users/p/"+str(user["personID"]))
        password=json.loads(response.text)
        if password:
            return User(id=user["personID"],email=user["email"],password=password["hash_pass"],bio=user["bio"],fname=user["fname"],lname=user["lname"],is_admin=user["is_admin"])
    return None
def users_all(): #read all users
    db=get_db()
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Users;')
    users=cursor.fetchall()
    user_api=[]
    for i in users:
        user_api.append({"id":i[0],"fname":i[1],"lname":i[2],"email":i[3],"is_admin":i[4],"bio":i[5]})
    return jsonify(user_api)
def user_one(data):#read one user
    db=get_db()
    cursor=db.cursor()
    if data.find("@")==-1:
        cursor.execute("SELECT * FROM Users WHERE personID = %s;",(data,))
    else:
        cursor.execute("SELECT * FROM Users WHERE e_mail = %s;",(data,))
    that_user=cursor.fetchone()
    if that_user:
        user_api={"personID":that_user[0],"fname":that_user[1],"lname":that_user[2],"email":that_user[3],"is_admin":that_user[4],"bio":that_user[5]}
    else:
        cursor.close()
        db.close()
        return {"error":"Not Found"}, 404
    cursor.close()
    db.close()
    return jsonify(user_api)
def insert_one_user(data):#create one user
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
    db.close()
    return data,201
def delete_user(data):#delete one user
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Users WHERE personID = %s",(data,))
    person=cursor.fetchone()
    if(not person):
        return {"error":"User not exists"},404
    cursor.execute("DELETE FROM Passes WHERE personID=%s",(person[0],))
    cursor.execute("SELECT * FROM Posts_ids WHERE personID = %s",(person[0],))
    posts_of_person=cursor.fetchall()
    cursor.execute("DELETE FROM Attendee_list WHERE personID=%s",(person[0],))
    cursor.execute("DELETE FROM Friends_of_user WHERE personID=%s",(person[0],))
    cursor.execute("DELETE FROM Friends_of_user WHERE personID=%s",(person[0],))
    cursor.execute("DELETE FROM Friends_of_user WHERE FriendID=%s",(person[0],))
    for i in posts_of_person:
        cursor.execute("DELETE FROM Comments_list WHERE postID=%s",(i[0],))
        if i[2]==0:
            cursor.execute("DELETE FROM Posts WHERE postID=%s",(i[0],))
        elif i[2]==1:
            cursor.execute("DELETE FROM Events WHERE postID=%s",(i[0],))
        elif i[2]==2:
            cursor.execute("DELETE FROM Items WHERE postID=%s",(i[0],))
    cursor.execute("DELETE FROM Posts_ids WHERE personID=%s",(person[0],))
    cursor.execute("DELETE FROM Users WHERE personID=%s",(person[0],))
    cursor.close()
    db.commit()
    db.close()
    return {"succes":"user deleted"},200
def update_one_user(data,payload):#update one user
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Users WHERE personID = %s",(data,))
    person=cursor.fetchone()
    if(not person):
        return {"error":"User not exists"},404
    cursor.execute("SELECT hash_pass FROM Passes WHERE personID = %s",(data,))
    hash_pass=cursor.fetchall()
    password=hash_pass[0][0]
    person_dict={
        "personID":person[0],
        "fname":person[1],
        "lname":person[2],
        "email":person[3],
        "is_admin":person[4],
        "bio":person[5],
        "password":password
    }
    for key1 in person_dict:
        for key2 in payload:
            if key1==key2:
                person_dict[key1]=payload[key2]
    cursor.execute("UPDATE Users SET F_name=%(fname)s,L_name=%(lname)s,e_mail=%(email)s,is_admin=%(is_admin)s,bio=%(bio)s WHERE personID=%(personID)s",person_dict)
    cursor.execute("UPDATE Passes SET hash_pass=%(password)s WHERE personID=%(personID)s",person_dict)
    cursor.close()
    db.commit()
    db.close()
    return jsonify(person_dict)
def auth_check(personID):#auth check
        db=get_db()
        cursor=db.cursor()
        cursor.execute("SELECT hash_pass FROM Passes WHERE personID=%s",(personID,))

        user_pass=cursor.fetchone()
        cursor.close()
        db.close()
        return {"hash_pass":user_pass},200
def send_friendship(data):
    db=get_db()
    cursor=db.cursor()
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        friend_req=json.loads(json_data)
    elif(isinstance(json_data,dict)):
        friend_req=json_data
    friend_req.update({"personID":data})
    cursor.execute("INSERT INTO Friends_of_user (personID,FriendID,accepted) VALUES (%(personID)s,%(FriendID)s,%(accepted)s)",friend_req)
    cursor.execute("INSERT INTO Friends_of_user (personID,FriendID,accepted) VALUES (%(FriendID)s,%(personID)s,%(accepted)s)",friend_req)
    cursor.execute("SELECT FriendshipID FROM Friends_of_user WHERE personID=%(personID)s AND FriendID=%(FriendID)s",friend_req)
    newly_inserted=cursor.fetchone()
    friend_req.update({"FriendshipID":newly_inserted[0]})
    cursor.close()
    db.commit()
    db.close()
    return jsonify(friend_req)
def accept_friendship(data):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Friends_of_user WHERE FriendshipID=%s",(data,))
    response=cursor.fetchone()
    cursor.execute("UPDATE Friends_of_user SET accepted=TRUE WHERE personID=%s AND FriendID=%s",(response[0],response[1],))
    cursor.execute("UPDATE Friends_of_user SET accepted=TRUE WHERE personID=%s AND FriendID=%s",(response[1],response[0],))
    cursor.close()
    db.commit()
    db.close()
    return jsonify({"success":"friends are shipped"})
def delete_friendship(data):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Friends_of_user WHERE FriendshipID=%s",(data,))
    response=cursor.fetchone()
    cursor.execute("DELETE FROM Friends_of_user WHERE personID=%s AND FriendID=%s",(response[0],response[1],))
    cursor.execute("DELETE FROM Friends_of_user WHERE personID=%s AND FriendID=%s",(response[1],response[0],))
    cursor.close()
    db.commit()
    db.close()
    return jsonify({"success":"friendship is destroyed"})
def get_users_friends(data):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Friends_of_user WHERE personID=%s AND accepted=TRUE",(data,))
    response=cursor.fetchall()
    result=[]
    for i in response:
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(i[1],))
        friend_data=cursor.fetchone()
        result.append({"FriendshipID":i[2],"personID":i[0],"FriendID":i[1],"accepted":i[3],"friend_data":{"personID":friend_data[0],"fname":friend_data[1],"lname":friend_data[2],"email":friend_data[3]}})
    cursor.close()
    db.close()
    return jsonify(result)
def friendship_requests(data):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Friends_of_user WHERE personID=%s AND accepted=FALSE",(data,))
    response=cursor.fetchall()
    result=[]
    for i in response:
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(i[1],))
        friend_data=cursor.fetchone()
        result.append({"FriendshipID":i[2],"personID":i[0],"FriendID":i[1],"accepted":i[3],"friend_data":{"personID":friend_data[0],"fname":friend_data[1],"lname":friend_data[2],"email":friend_data[3]}})
    cursor.close()
    db.close()
    return jsonify(result)