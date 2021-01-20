from DB_call import get_db
from flask import jsonify,request
import json
import requests
def new_post():#add post
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        data=json.loads(json_data)
    elif(isinstance(json_data,dict)):
        data=json_data
    db=get_db()
    cursor=db.cursor()
    try:
        cursor.execute("INSERT INTO Posts_ids (personID,iem_type) VALUES (%(personID)s,%(type)s)",data)
        cursor.execute("SELECT MAX(postID) FROM Posts_ids WHERE personID=%(personID)s",data)
        postID=cursor.fetchone()
        data.update({"postID":postID[0]})
        if data["type"]=="0":
            cursor.execute("INSERT INTO Posts (postID,payload,is_news) VALUES (%(postID)s,%(payload)s,%(is_news)s)",data)
        elif data["type"]=="1":
            cursor.execute("INSERT INTO Events (postID,payload) VALUES (%(postID)s,%(payload)s)",data)
        elif data["type"]=="2":
            cursor.execute("INSERT INTO Items (postID,payload,price) VALUES (%(postID)s,%(payload)s,%(price)s)",data)
        cursor.close()
        db.commit()
    except:
        return {"error":"error occured"},400
    return data,200
def get_all_posts():#get all of the posts
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Posts")
    Posts=cursor.fetchall()
    cursor.execute("SELECT * FROM Events")
    Events=cursor.fetchall()
    cursor.execute("SELECT * FROM Items")
    Items=cursor.fetchall()
    all_posts={
        "posts":[],
        "events":[],
        "items":[]
    }
    for i in Posts:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        post={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"is_news":i[2],"publish_date":i[3]}
        all_posts["posts"].append(post)
    for i in Events:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        event={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"publish_date":i[2]}
        all_posts["events"].append(event)
    for i in Items:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        item={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"price":i[2],"publish_date":i[3]}
        all_posts["items"].append(item)
    return jsonify(all_posts)
def get_one_post(data):#get one post
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Posts WHERE postID=%s",(data,))
    Posts=cursor.fetchone()
    cursor.execute("SELECT * FROM Events WHERE postID=%s",(data,))
    Events=cursor.fetchone()
    cursor.execute("SELECT * FROM Items WHERE postID=%s",(data,))
    Items=cursor.fetchone()
    cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(data,))
    personID=cursor.fetchone()
    cursor.execute("SELECT F_name,L_name FROM Users WHERE personID=%s",(personID[0],))
    name=cursor.fetchone()
    res_dict={}
    if(Posts):
        res_dict={"name":name[0]+" "+name[1],"postID":Posts[0],"payload":Posts[1],"is_news":Posts[2],"publish_date":Posts[3]}
    elif(Events):
        res_dict={"name":name[0]+" "+name[1],"postID":Events[0],"payload":Events[1],"publish_date":Events[2]}
    elif(Items):
        res_dict={"name":name[0]+" "+name[1],"postID":Items[0],"payload":Items[1],"price":Items[2],"publish_date":Items[3]}
    else:
        return {"error":"no post found"},404
    return jsonify(res_dict)
def update_post(data):#update one post
    json_data=request.get_json()
    if(isinstance(json_data,str)):
        post=json.loads(json_data)
    elif(isinstance(json_data,dict)):
        post=json_data
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Posts_ids WHERE postID = %s",(data,))
    post_root=cursor.fetchone()
    if(not post_root):
        return {"error":"User not exists"},404
    if str(post_root[2])=="0":
        cursor.execute("SELECT * FROM Posts WHERE postID=%s",(post_root[0],))
        post_data=cursor.fetchone()
        post_dict={
            "postID":post_data[0],
            "payload":post_data[1],
            "is_news":post_data[2],
            "date":post_data[3]
        }
    elif str(post_root[2])=="1":
        cursor.execute("SELECT * FROM Events WHERE postID=%s",(post_root[0],))
        post_data=cursor.fetchone()
        post_dict={
            "postID":post_data[0],
            "payload":post_data[1],
            "date":post_data[2]
        }
    elif str(post_root[2])=="2":
        cursor.execute("SELECT * FROM Items WHERE postID=%s",(post_root[0],))
        post_data=cursor.fetchone()
        post_dict={
            "postID":post_data[0],
            "payload":post_data[1],
            "price":post_data[2],
            "date":post_data[3]
        }
    for key1 in post_dict:
        for key2 in post:
            if key1==key2:
                post_dict[key1]=post[key2]
    if str(post_root[2])=="0":
        cursor.execute("UPDATE Posts SET payload=%(payload)s,is_news=%(is_news)s,publish_date=CURRENT_TIMESTAMP WHERE postID=%(postID)s",post_dict)
    elif str(post_root[2])=="1":
            cursor.execute("UPDATE Events SET payload=%(payload)s,publish_date=CURRENT_TIMESTAMP WHERE postID=%(postID)s",post_dict)
    elif str(post_root[2])=="2":
        cursor.execute("UPDATE Items SET payload=%(payload)s,price=%(price)s,publish_date=CURRENT_TIMESTAMP WHERE postID=%(postID)s",post_dict)
    cursor.close()
    db.commit()
    return jsonify(post_dict)
def delete_post(data):#delete post
    db=get_db()
    cursor=db.cursor()
    try:
        cursor.execute("SELECT * FROM Posts_ids WHERE postID=%s",(data,))
        post_root=cursor.fetchone()
        if not post_root:
            return{"error":"post not found"},404
        if str(post_root[2])=="0":
            cursor.execute("DELETE FROM Posts WHERE postID=%s",(post_root[0],))
        elif str(post_root[2])=="1":
            cursor.execute("DELETE FROM Events WHERE postID=%s",(post_root[0],))
        elif str(post_root[2])=="2":
            cursor.execute("DELETE FROM Items WHERE postID=%s",(post_root[0],))
        cursor.execute("DELETE FROM Posts_ids WHERE postID=%s",(post_root[0],))
        cursor.close()
        db.commit()
        return {"success":"Post deleted"},200
    except:
        return {"error":"an error occured"},400
def get_friends_posts(data):#get all posts from users friends
    db=get_db()
    cursor=db.cursor()
    cursor.execute("SELECT tb3.* FROM Posts tb3 INNER JOIN ( SELECT tb1.postID FROM Posts_ids tb1 INNER JOIN Friends_of_user tb2 ON tb1.personID=tb2.FriendID AND tb2.personID=%s AND tb2.accepted=TRUE) tb4 ON tb4.postID=tb3.postID",(data,))
    posts=cursor.fetchall()
    cursor.execute("SELECT tb5.* FROM Events tb5 INNER JOIN ( SELECT tb1.postID FROM Posts_ids tb1 INNER JOIN Friends_of_user tb2 ON tb1.personID=tb2.FriendID AND tb2.personID=%s AND tb2.accepted=TRUE) tb6 ON tb5.postID=tb6.postID",(data,))
    events=cursor.fetchall()
    cursor.execute("SELECT tb7.* FROM Items tb7 INNER JOIN ( SELECT tb1.postID FROM Posts_ids tb1 INNER JOIN Friends_of_user tb2 ON tb1.personID=tb2.FriendID AND tb2.personID=%s AND tb2.accepted=TRUE) tb8 ON tb7.postId=tb8.postID",(data,))
    items=cursor.fetchall()
    all_posts={
        "posts":[],
        "events":[],
        "items":[],
    }
    for i in posts:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        post={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"is_news":i[2],"publish_date":i[3]}
        all_posts["posts"].append(post)
    for i in events:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        event={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"publish_date":i[2]}
        all_posts["events"].append(event)
    for i in items:
        cursor.execute("SELECT personID FROM Posts_ids WHERE postID=%s",(i[0],))
        personID=cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE personID=%s",(personID[0],))
        user=cursor.fetchone()
        item={"user_info":{"personID":user[0],"Name":user[1]+" "+user[2],"email":user[3]},"postID":i[0],"payload":i[1],"price":i[2],"publish_date":i[3]}
        all_posts["items"].append(item)
    return jsonify(all_posts)





