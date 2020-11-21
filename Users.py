from DB_call import get_db
from flask import jsonify
def users_all():
    db=get_db()
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Users;')
    users=cursor.fetchall()
    user_api={}
    for i in users:
        user_api.update({i[0]:{"first_name":i[1],"last_name":i[2],"email":i[3]}})
    return jsonify(user_api)
def user_one(personID):
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Users WHERE personID = %s;",(personID,))
    that_user=cursor.fetchone()
    if that_user:
        user_api={that_user[0]:{"first_name":that_user[1],"last_name":that_user[2],"email":that_user[3]}}
    else:
        return "<h1>404</h1><p>The resource could not be found.</p>", 404
    return jsonify(user_api)
#def auth_check(personID):