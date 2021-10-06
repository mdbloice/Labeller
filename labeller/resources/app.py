# app.py
# Author: Labeller <https://github.com/mdbloice/Labeller>
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, g, request, abort, jsonify
import os
import glob
import random
import sqlite3
import sys

app = Flask(__name__)
Bootstrap(app)

# Read the config file which contains the class names.
# NOT CURRENTLY NEEDED
#with open('labeller.pkl', 'rb') as to_read:
#    class_names = pickle.load(to_read)

# Global
randomised = False

# SQLite Database
DATABASE = os.path.join('.', 'db', 'labels.db')
ROOT_IMAGE_PATH = os.path.join('.', 'static', 'images')

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

# Function to remove all images that have already been labelled
# Not currently used.
#def remove_labelled_images():
#    for image in images:
#        image = str.split(image, os.path.join(ROOT_IMAGE_PATH, os.sep))[-1]
#        with app.app_context():
#            con = get_db()
#            cursor = con.cursor()
#            cursor.execute('SELECT EXISTS(SELECT 1 FROM labels WHERE image="%s" LIMIT 1);' % image)
#            data=cursor.fetchall()
#            if data[0][0]:
#                print("Labelled since last reload: %s" % os.path.join(ROOT_IMAGE_PATH, image))
#                images.remove(os.path.join(ROOT_IMAGE_PATH, image))
#            cursor.close()

@app.route('/api/image', methods=['POST'])
def set_image():

    if not request.json or not 'image' in request.json or not 'label' in request.json or not 'label_string' in request.json:
        abort(400)

    q = "INSERT INTO labels (image, label, label_string) VALUES ('%s', %s, '%s')"  \
        % (request.json['image'].split('images/')[-1], request.json['label'], request.json['label_string'])

    con =  get_db()
    cursor = con.cursor()
    cursor.execute(q)
    con.commit()
    cursor.close()

    return jsonify({"Status": "OK"})

@app.route('/')
def index():
        # Perform all image searching here in the index rather than
        # outside of any of the routes
        extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
        images = []

        for ext in extensions:
            images.extend(glob.glob(os.path.join(ROOT_IMAGE_PATH, ext)))

        total_n_images = len(images)  # Total number of images labelled or unlabelled

        images_to_remove = []

        for image in images:

            image = str.split(image, os.path.join(ROOT_IMAGE_PATH, os.sep))[-1]
            con = get_db()
            cursor = con.cursor()
            cursor.execute('SELECT EXISTS(SELECT 1 FROM labels WHERE image="%s" LIMIT 1);' % image)
            data=cursor.fetchall()

            if data[0][0] == 1:
                images_to_remove.append(os.path.join(ROOT_IMAGE_PATH, image))

            cursor.close()

        print("Length of images to remove: %s" % len(images_to_remove))

        # This is happening for every refresh and page visit, we may need to fix that.
        images = list(set(images) - set(images_to_remove))

        # Randomise the order of the images, only once if not done before.
        global randomised
        if not randomised:
            print("Randomising image list...")
            random.shuffle(images)
            randomised = True

        remaining_image_count = len(images)

        return render_template(
        'index.html', images=images, remaining_image_count=remaining_image_count, total_n_images=total_n_images)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/labels.html')
def labels():
    labels = query_db("SELECT * FROM labels")
    return render_template('labels.html', labels=labels)

#if __name__ == '__main__':
#    app.run(debug=False, use_reloader=False, port=5000)