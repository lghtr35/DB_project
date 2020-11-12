from flask import Flask,render_template,url_for,request,g
import mysql.connector
from datetime import datetime
import hashlib
db=mysql.connector.connect(
        host="localhost",
        user="root",
        password="sanane22021999",
        database="Itu_soc_app"
    )
def createApp():
    app=Flask(__name__)
    app.config["DEBUG"] = True
    app.config["PORT"] = 8080
    app.add_url_rule("/", view_func=home_page,methods=['GET','POST'])
    app.add_url_rule("/profile/<int:personID>", view_func=my_page,methods=['GET','POST'])
    app.add_url_rule("/signup",view_func=signup_page,methods=['POST','GET'])
    return app
def home_page():
    cursor=db.cursor()
    cursor.execute('SELECT post_data,personID,name_author,pub_date FROM Posts;')
    tables=cursor.fetchall()
    print(tables)
    if request.method == 'POST':
        post_data=request.form('post_data')
        cursor.execute("INSERT INTO Posts (post_data,personID,name_author) VALUES ('%s',%s,'%s');",post_data,12,'me and myself')
    cursor.close()
    return render_template("home.html",payload=tables)
def my_page(personID):
    return render_template("profile.html")
def signup_page():
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
    app.run(host="0.0.0.0",port=8080,debug=True)