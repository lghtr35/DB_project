from flask import Flask,render_template,url_for,request,g,jsonify
import mysql.connector
from datetime import datetime
from Users import users_all,user_one
from DB_call import get_db
import hashlib
import json
def createApp():
    app=Flask(__name__)
    app.config["DEBUG"] = True
    app.config["PORT"] = 8080
    app.add_url_rule("/", view_func=home_page,methods=['GET','POST'])
    app.add_url_rule("/profile", view_func=my_page,methods=['GET','POST'])
    app.add_url_rule("/signup",view_func=signup_page,methods=['POST','GET'])
    app.add_url_rule("/users/all",view_func=users_all,methods=['GET'])
    app.add_url_rule("/users/<int:personID>",view_func=user_one,methods=['GET'])
    return app
def home_page():
    payload=users_all()
    return render_template("home.html",payload=payload)
def my_page():
    return render_template("profile.html")
def signup_page():
    db=get_db()
    cursor=db.cursor()
    if request.method=='POST':
        cursor.execute('SELECT COUNT(personID) FROM Users;')
        count=cursor.fetchone()
        print(count)
        personID=1
        firstname=request.form['fname']
        lastname=request.form['lname']
        email=request.form['email']
        cursor.execute("INSERT INTO Users (personID,Firstname,Lastname,email) VALUES(%s '%s' '%s' '%s');",(personID,firstname,lastname,email))
        hashpass=hashlib.md5(request.form['password'].encode())
        cursor.execute("INSERT INTO Passes (personID,pass) VALUES('%s' '%s');",(personID,str(hashpass)))
    return render_template("signup.html")
if __name__=="__main__":
    app=createApp()
    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404
    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()
    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404
    app.run(host="0.0.0.0",port=8080,debug=True)