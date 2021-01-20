from flask import Flask,render_template,url_for,request,g,jsonify,redirect
from Users import users_all,user_one,User,get_User_obj,insert_one_user,update_one_user
import requests
from flask_login import login_required,login_user,current_user
import json
from passlib.hash import pbkdf2_sha256
def post_user():
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        post=json.loads(json_data)
        response=insert_one_user(post)
    elif(isinstance(json_data,dict)):
        password=str(json_data["password"])
        password=pbkdf2_sha256.hash(password)
        json_data["password"]=password
        response=insert_one_user(json_data)
    return(response)
def update_user(data):
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        post=json.loads(json_data)
        if("password" in post):
            password=str(post["password"])
            post["password"]=password
        response=update_one_user(data,post)
    elif(isinstance(json_data,dict)):
        if("password" in json_data):
            password=str(json_data["password"])
            password=pbkdf2_sha256.hash(password)
            json_data["password"]=password
        response=update_one_user(data,json_data)
    return(response)
@login_required
def home_page():

    post_button=request.form.get("post_button")
    radio=request.form.get("radio")
    text=request.form.get("payload")
    is_news=request.form.get("is_news")
    if(post_button):
        post={
            "payload":text,
            "personID":current_user.id
        }
        if radio == "Post":
            post.update({"is_news":True if is_news else False,"type":"0"})
        elif radio == "Event":
            post.update({"type":"1"})
        elif radio =="Item":
            price=request.form["price"]
            post.update({"price":str(price),"type":"2"})
        response=requests.post(url=request.host_url+"/api/posts/",json=json.dumps(post))
        payload=json.loads(requests.get(request.host_url+"/api/posts/frnd/"+str(current_user.id)).text)
        return render_template("home.html",payload=payload)
    payload=json.loads(requests.get(request.host_url+"/api/posts/frnd/"+str(current_user.id)).text)
    return render_template("home.html",payload=payload)
def login_page():
    if request.method=="POST":
        email=request.form["email"]
        password=str(request.form["password"])
        user=get_User_obj(email)
        if user:
            if pbkdf2_sha256.verify(str(password),str(user.password[0])):
                login_user(user)
                return redirect(url_for("home_page"))
            else:
                return redirect(url_for("login_page"))
        else:
            return redirect(url_for("login_page"))
    return render_template("login.html")
@login_required
def my_page():
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    bio=request.form.get("bio")
    email=request.form.get("email")
    password=request.form.get("password")
    accept=request.form.get("accept")
    reject=request.form.get("reject")
    if(accept):
        accept_resp=requests.put(url=request.host_url+"/api/frnd/"+str(accept))
    if(reject):
        reject_resp=requests.delete(url=request.host_url+"/api/frnd/"+str(reject))
    temp={}
    temp.update({"fname":fname,"lname":lname,"bio":bio,"email":email,"password":password})
    person={}
    for i in temp:
        if temp[i]!="":
            person.update({i:temp[i]})
    submit=request.form.get("Submit")
    if(submit):
        response=requests.put(url=request.host_url+"/api/users/"+str(current_user.id),json=json.dumps(person))
        payload=json.loads(requests.get(request.host_url+"/api/users/"+str(current_user.id)).text)
        posts_of_user=json.loads(requests.get(request.host_url+"/api/posts/").text)
        return render_template("profile.html",payload=[payload,False])
    cancel=request.form.get("cancel")
    if(cancel):
        payload=json.loads(requests.get(request.host_url+"/api/users/"+str(current_user.id)).text)
        posts_of_user=json.loads(requests.get(request.host_url+"/api/posts/").text)
        return render_template("profile.html",payload=[payload,False])
    clicked=request.form.get("edit")
    if(clicked):
        payload=json.loads(requests.get(request.host_url+"/api/users/"+str(current_user.id)).text)
        posts_of_user=json.loads(requests.get(request.host_url+"/api/posts/").text)
        return render_template("profile.html",payload=[payload,True])
    payload=json.loads(requests.get(request.host_url+"/api/users/"+str(current_user.id)).text)
    posts_of_user=json.loads(requests.get(request.host_url+"/api/posts/").text)
    friends=json.loads(requests.get(request.host_url+"/api/frnd/accptd/"+str(current_user.id)).text)
    friend_reqests=json.loads(requests.get(request.host_url+"/api/frnd/not/"+str(current_user.id)).text)
    return render_template("profile.html",payload=[payload,False],posts_of_user=posts_of_user,fr_req=friend_reqests,friends=friends)    
@login_required
def discover_page():
    payload=json.loads(requests.get(request.host_url+"/api/posts").text)
    return render_template("discover.html",payload=payload)        
@login_required
def person_page(data):
    if(str(current_user.id)==str(data)):
        return redirect(url_for("my_page"))
    add_friend=request.form.get("add_friend")
    if(add_friend):
        fr_req={"FriendID":str(add_friend),"accepted":False}
        response=requests.post(url=request.host_url+"/api/frnd/"+str(current_user.id),json=json.dumps(fr_req))
    friends=json.loads(requests.get(request.host_url+"/api/frnd/accptd/"+str(current_user.id)).text)
    are_u_fr=True
    for i in friends:
        if str(i["FriendID"])==str(data):
            are_u_fr=False
    payload=json.loads(requests.get(request.host_url+"/api/users/"+str(data)).text)
    return render_template("person.html",payload=[payload,False],friends=are_u_fr)  
def signup_page():
    error_bool=False
    if request.method == "POST":
        email=request.form["email"]
        if email:
            temp=email.split("@")
            if temp[1]=="itu.edu.tr":
                password=request.form["password"]
                fname=request.form.get("fname")
                lname=request.form.get("lname")
                bio=request.form.get("bio")
                post={"email":email,
                "password":pbkdf2_sha256.hash(password),
                "fname":fname,
                "lname":lname,
                "bio":bio,
                "is_admin":False}
                response=requests.post(url=request.host_url+"/api/users/add",json=json.dumps(post))
                return render_template("signup.html",error_message=error_bool)
            else:
                error_bool=True
        return render_template("signup.html",error_message=error_bool)
    else:
        return render_template("signup.html",error_message=error_bool)