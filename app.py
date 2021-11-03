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
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'wrong password'})

@app.route('/registerpage', methods=['POST'])
def register():
    post_data = request.get_json()
    x = post_data.get('username')
    y = post_data.get('password')
    doc = mongo.db.user.insert({'username': x, 'password': y, 'friendlist':[]})
    print(x,y)

    return jsonify({'status': 'success'})

@app.route('/getlist', methods=['POST'])
def getlist():
    post_data = request.get_json()
    x = post_data.get('username')
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

@app.route('/updatelist', methods=['POST'])
def updatelist():
    post_data = request.get_json()
    x = post_data.get('username')
    y = post_data.get('friendname')
    z = post_data.get('friendemail')
    print(x,y,z)
    doc = mongo.db.user.find_one({'username':x})
    flist = doc['friendlist']
    
    print("flist: ", flist)

    for account in flist:
        print("account: ", account)
        if account['name'] == y:
            account['email'] = z
            newvalues = { "$set": { "friendlist": flist } }
            mongo.db.user.update_one({'username':x},newvalues)
            return jsonify({ 'status': 'success' })
    
    flist.append({'name':y,'email':z})
    newvalues = { "$set": { "friendlist": flist } }
    mongo.db.user.update_one({'username':x},newvalues)

    return jsonify({
        'status': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True)