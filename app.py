from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/user")

@app.route('/')
def index():
    title = '試驗網站'
    list = [
        'one',
        'two',
        'three'
    ]
    return render_template('base.html', title = title, data = list)

@app.route('/edit.html')
def edit():
    return render_template('edit.html')

@app.route('/user.html')
def user():
    return render_template('user.html')

@app.route('/register.html')
def regis():
    return render_template('register.html')
    
@app.route('/loginpage', methods=['POST'])

def login():
    post_data = request.get_json()
    x = post_data.get('username')
    y = post_data.get('password')
    print(x,y)
    doc = mongo.db.user.find_one({'username':x})
    if doc==None:
        return jsonify({'status': '賬號不存在'})
    if(doc['username']==x and doc['password']==y):
        doc = mongo.db.users.update_one({'now_user': ''},{ "$set": { "now_user": x } })
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'wrong password'})

@app.route('/registerpage', methods=['POST'])
def register():
    post_data = request.get_json()
    x = post_data.get('username')
    y = post_data.get('password')
    doc = mongo.db.user.find_one({'username':x})
    if doc!=None:
        return jsonify({'status': 'fail'})
    doc = mongo.db.user.insert({'username': x, 'password': y, 'friendlist':[]})
    print(x,y)
    doc = mongo.db.users.update_one({'now_user': ''},{ "$set": { "now_user": x } })
    return jsonify({'status': 'success'})

@app.route('/logout', methods=['POST'])
def logout():
    doc = mongo.db.users.find_one({})
    print('logout: ',doc['now_user'])
    mongo.db.users.update_one({'now_user': doc['now_user']},{ "$set": { "now_user": '' } })
    return jsonify({'status': 'success'})
@app.route('/getlist', methods=['POST'])
def getlist():
    now_user = mongo.db.users.find_one({})
    x = now_user['now_user']
    print(x)
    doc = mongo.db.user.find_one({'username':x})
    print(doc)
    if doc==None:
        return jsonify({'status': '賬號不存在'})
    return jsonify({
        'status': 'success',
        'username': doc['username'],
        'friendlist': doc['friendlist']
    })


@app.route('/addlist', methods=['POST'])
def addlist():
    post_data = request.get_json()
    now_user = mongo.db.users.find_one({})
    x = now_user['now_user']
    y = post_data.get('friendname')
    z = post_data.get('friendemail')
    print(x,y,z)
    doc = mongo.db.user.find_one({'username':x})
    flist=doc['friendlist']
    leng=len(flist)
    if leng!=0:
        leng=flist[leng-1]['id']+1
    flist.append({'id':leng,'name':y,'email':z})
    print(flist)
    newvalues = { "$set": { "friendlist": flist } }
    mongo.db.user.update_one({'username':x},newvalues)
    return jsonify({
        'status': 'success'
    })

@app.route('/updatelist', methods=['POST'])
def updatelist():
    post_data = request.get_json()
    now_user = mongo.db.users.find_one({})
    x = now_user['now_user']
    i = post_data.get('friendid')
    y = post_data.get('friendname')
    z = post_data.get('friendemail')
    print(x,y,z,i)
    doc = mongo.db.user.find_one({'username':x})
    print(doc)
    flist = doc['friendlist']
    
    print("flist: ", flist)

    for account in flist:
        print("account: ", account['id'],i)
        if account['id'] == int(i):
            print('hey')
            account['name'] = y
            account['email'] = z

    newvalues = { "$set": { "friendlist": flist } }
    mongo.db.user.update_one({'username':x},newvalues)

    return jsonify({
        'status': 'success'
    })

@app.route('/deletelist', methods=['POST'])
def deletelist():
    post_data = request.get_json()
    now_user = mongo.db.users.find_one({})
    x = now_user['now_user']
    i = post_data.get('friendid')
    doc = mongo.db.user.find_one({'username':x})
    flist = doc['friendlist']
    cnt=0
    while flist[cnt]['id']!=i:
        cnt+=1
    print(flist)
    flist.pop(cnt)
    print(flist)
    
    newvalues = { "$set": { "friendlist": flist } }
    mongo.db.user.update_one({'username':x},newvalues)
    return jsonify({
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(port=5000,debug=True)