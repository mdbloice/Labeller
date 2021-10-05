# app.py
# Author: Labeller <https://github.com/mdbloice/Labeller>
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, g, request, abort, jsonify
import os
import glob
import random
import sqlite3

app = Flask(__name__)
Bootstrap(app)

# Read the config file which contains the class names.
# NOT CURRENTLY NEEDED
#with open('labeller.pkl', 'rb') as to_read:
#    class_names = pickle.load(to_read)

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

extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
images = []
for ext in extensions:
    images.extend(glob.glob(os.path.join(ROOT_IMAGE_PATH, ext)))

print("Found %s images." % len(images))

total_n_images = len(images)
total_remaining_images = len(images)

# Randomise the order of the images
random.shuffle(images)

# Function to remove all images that have already been labelled
def remove_labelled_images():
    for image in images:
        image = str.split(image, os.path.join(ROOT_IMAGE_PATH, os.sep))[-1]
        with app.app_context():
            con = get_db()
            cursor = con.cursor()
            cursor.execute('SELECT EXISTS(SELECT 1 FROM labels WHERE image="%s" LIMIT 1);' % image)
            data=cursor.fetchall()
            if data[0][0]:
                print("Labelled since last reload: %s" % os.path.join(ROOT_IMAGE_PATH, image))
                images.remove(os.path.join(ROOT_IMAGE_PATH, image))
            cursor.close()

# Remove images that have already been labelled:
remove_labelled_images()

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
        image_count = len(images)
        # Because we have already shuffled the images, we will pass the first
        # image in the list as the random initial image
        # rand_image= images[random.randint(0, image_count-1)]

        # Here we need to double check if any more images have been labelled
        remove_labelled_images()

        return render_template(
        'index.html', images=images, image_count=image_count, total_n_images=total_n_images)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/labels.html')
def labels():
    labels = query_db("SELECT * FROM labels")
    return render_template('labels.html', labels=labels)

#if __name__ == '__main__':
#    app.run(debug=False, use_reloader=False, port=5000)