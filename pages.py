from flask import Flask,render_template,url_for,request,g,jsonify
from API import users_all,user_one,post_user,salt
from Users import User,All_users
import requests
def home_page():
    All_user_object=All_users()
    payload=All_user_object.get_all_users()
    return render_template("home.html",payload=payload[0])
def login_page():
    return render_template("login.html")
def my_page():
    return render_template("profile.html")
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
                All_user_object=All_users()
                new_user=User(email=email,fname=fname,lname=lname,bio=bio,is_admin=False,password=password)
                All_user_object.post_new_user(new_user)
                return render_template("signup.html",error_message=error_bool)
            else:
                error_bool=True
        return render_template("signup.html",error_message=error_bool)
    else:
        return render_template("signup.html",error_message=error_bool)