from flask import Flask,render_template,url_for,request,g,jsonify
from pages import home_page,my_page,signup_page,login_page
from API import users_all,user_one,post_user
from flask_login import LoginManager

lm=LoginManager()
@lm.user_loader
def load_user(personID):
    return user_one(personID)

app=Flask(__name__)
app.add_url_rule("/", view_func=home_page)
app.add_url_rule("/profile", view_func=my_page)
app.add_url_rule("/signup",view_func=signup_page,methods=['GET','POST'])
app.add_url_rule("/login",view_func=login_page,methods=['GET','POST'])
app.add_url_rule("/api/users/",view_func=users_all,methods=['GET'])
app.add_url_rule("/api/users/<int:personID>",view_func=user_one,methods=['GET'])
app.add_url_rule("/api/users/add",view_func=post_user,methods=['POST'])
lm.init_app(app)
lm.login_view="login_page"

if __name__=="__main__":
    app.run(port=8080,debug=True)