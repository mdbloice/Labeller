# app.py
# Author: Labeller <https://github.com/mdbloice/Labeller>
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import os
import glob
import random

app = Flask(__name__)
Bootstrap(app)

# Read tiles
#list_of_tiles = glob.glob(os.path.join('.', 'images', '*.jpg'))
#
#extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
#list_of_tiles = []
#for ext in extensions:
#    list_of_tiles.extend(glob.glob(os.path.join('.', 'images', ext)))

#print("Found %s images." % len(list_of_tiles))

#DATABASE = os.path.join('.', 'db', 'tags.db')

#def get_db():
#    db = getattr(g, '_database', None)
#
#    if db is None:
#        db = g._database = sqlite3.connect(DATABASE)
#    return db

#@app.teardown_appcontext
#def teardown_db(exception):
#    db = getattr(g, '_database', None)
#
#    if db is not None:
#        db.close()

#def query_db(query, args=(), one=False):
#    # See: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#    # Usage for single result:
#    # user = query_db('select * from users where username = ?', [the_username], one=True)
#    # For normal usage:
#    # for user in query_db('select * from users'):
#    #    print user['username'], 'has the id', user['user_id']
#    cur = get_db().execute(query, args)
#    rv = cur.fetchall()
#    cur.close()
#    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():

        tile_count = len(list_of_tiles)
        r = random.randint(0, tile_count-1)
        rand_tile = list_of_tiles[r]

        return render_template(
        'index.html', list_of_tiles=list_of_tiles,
        rand_tile=rand_tile, tile_count=tile_count, r=r)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/labels.html')
def labels():
    return render_template('labels.html')

#if __name__ == '__main__':
#    app.run(debug=False, use_reloader=False, port=5000)