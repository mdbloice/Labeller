# app.py
# Author: Labeller <https://github.com/mdbloice/Labeller>
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, g, request, abort, jsonify
import os
import glob
import random
import sqlite3
import pickle

app = Flask(__name__)
Bootstrap(app)

# Read the config file which contains the class names.
# NOT CURRENTLY NEEDED
#with open('labeller.pkl', 'rb') as to_read:
#    class_names = pickle.load(to_read)

extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
images = []
for ext in extensions:
    images.extend(glob.glob(os.path.join('.', 'static', 'images', ext)))

print("Found %s images." % len(images))

# SQLite Database
DATABASE = os.path.join('.', 'db', 'labels.db')

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/image', methods=['POST'])
def set_image():
    if not request.json or not 'tile' in request.json or not 'tag' in request.json:
        abort(400)

    q = "INSERT INTO labels (image, label, label_string) VALUES ('%s', %s)"  \
        % (request.json['tile'], request.json['tag'])

    con =  get_db()
    cursor = con.cursor()
    cursor.execute(q)
    con.commit()
    cursor.close()

    return jsonify({"Status": "OK"})

@app.route('/')
def index():
        image_count = len(images)
        r = random.randint(0, image_count-1)
        rand_image= images[r]

        return render_template(
        'index.html', images=images,
        rand_image=rand_image, image_count=image_count)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/labels.html')
def labels():
    labels = query_db("SELECT * FROM labels")
    return render_template('labels.html', labels=labels)

#if __name__ == '__main__':
#    app.run(debug=False, use_reloader=False, port=5000)