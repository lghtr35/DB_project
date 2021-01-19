from flask import Flask,render_template,url_for,request,g,jsonify,redirect,flash
from pages import home_page,my_page,signup_page,login_page,post_user,update_user,discover_page
from Users import users_all,user_one,auth_check,get_User_obj,delete_user,send_friendship,accept_friendship,delete_friendship,get_users_friends,friendship_requests
from Posts import new_post,delete_post,update_post,get_all_posts,get_one_post,get_friends_posts
from flask_login import LoginManager,current_user,logout_user

lm=LoginManager()
@lm.user_loader
def load_user(personID):
    return get_User_obj(personID)

def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for("login_page"))

app=Flask(__name__)
app.config['SECRET_KEY']='siteiste'
#Pages
app.add_url_rule("/", view_func=home_page,methods=['GET','POST'])
app.add_url_rule("/profile", view_func=my_page,methods=['GET','POST'])
app.add_url_rule("/signup",view_func=signup_page,methods=['GET','POST'])
app.add_url_rule("/login",view_func=login_page,methods=['GET','POST'])
app.add_url_rule("/logout",view_func=logout,methods=['GET','POST'])
app.add_url_rule("/discover",view_func=discover_page,methods=['GET','POST'])
#API
#   USER
app.add_url_rule("/api/users/",view_func=users_all,methods=['GET'])
app.add_url_rule("/api/users/<data>",view_func=user_one,methods=['GET'])
app.add_url_rule("/api/users/<data>",view_func=delete_user,methods=['DELETE'])
app.add_url_rule("/api/users/<data>",view_func=update_user,methods=['PUT'])
app.add_url_rule("/api/users/add",view_func=post_user,methods=['POST'])
app.add_url_rule("/api/users/p/<personID>",view_func=auth_check)
#   POSTS
app.add_url_rule("/api/posts/",view_func=get_all_posts,methods=['GET'])
app.add_url_rule("/api/posts/",view_func=new_post,methods=['POST'])
app.add_url_rule("/api/posts/<data>",view_func=delete_post,methods=['DELETE'])
app.add_url_rule("/api/posts/<data>",view_func=update_post,methods=['PUT'])
app.add_url_rule("/api/posts/<data>",view_func=get_one_post,methods=['GET'])
app.add_url_rule("/api/posts/frnd/<data>",view_func=get_friends_posts,methods=['GET'])
#   FRIEND
app.add_url_rule("/api/frnd/<data>",view_func=send_friendship,methods=['POST'])
app.add_url_rule("/api/frnd/accptd/<data>",view_func=get_users_friends,methods=['GET'])
app.add_url_rule("/api/frnd/not/<data>",view_func=friendship_requests,methods=['GET'])
app.add_url_rule("/api/frnd/<data>",view_func=accept_friendship,methods=['PUT'])
app.add_url_rule("/api/frnd/<data>",view_func=delete_friendship,methods=['DELETE'])
lm.init_app(app)
lm.login_view="login_page"

if __name__=="__main__":
    app.run(port=8080,debug=True)