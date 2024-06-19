from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Replace with your MongoDB connection string
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Ramachandra:Ramachandra2003@cluster0.hedzdql.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient(MONGO_URI)
db = client['testdb']
collection = db['testcollection']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            data = {'data': request.form['data']}
            collection.insert_one(data)
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error in /create: {e}")
            return jsonify({"error": str(e)}), 500
    return render_template('create.html')

@app.route('/read', methods=['GET'])
def read():
    try:
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data)
    except Exception as e:
        print(f"Error in /read: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        try:
            id = request.form['id']
            data = {'data': request.form['data']}
            collection.update_one({'_id': ObjectId(id)}, {'$set': data})
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error in /update: {e}")
            return jsonify({"error": str(e)}), 500
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        try:
            id = request.form['id']
            collection.delete_one({'_id': ObjectId(id)})
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error in /delete: {e}")
            return jsonify({"error": str(e)}), 500
    return render_template('delete.html')

@app.route('/test_mongo')
def test_mongo():
    try:
        # Attempt to retrieve a document
        doc = collection.find_one()
        if doc:
            return jsonify({"message": "MongoDB connection is successful"}), 200
        else:
            return jsonify({"message": "MongoDB connection is successful, but no data found"}), 200
    except Exception as e:
        print(f"Error in /test_mongo: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
