# labeller.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.
import argparse
import sys
import sqlite3
import os
from collections import OrderedDict
import pkg_resources

# Internal imports
from htmlElements import Footer, Tagger

parser = argparse.ArgumentParser(description='Generate an image labelling application.')
parser.add_argument('n_classes', metavar='n_classes', type=int, nargs=1, help='the number of classes')
parser.add_argument('class_names', metavar='class_names', nargs='+', help='a list of class names')
args = parser.parse_args()

if args.n_classes[0] <= 1:
    print('Minimum number of classes is 2.')
    sys.exit(1)

if args.n_classes[0] != len(args.class_names):
    print('Number of classes (%s) does equal number of class names provided (%s)' % (args.n_classes[0], len(args.class_names)))
    sys.exit(1)

print("Generated application with %s classes, with the labels %s" % (args.n_classes[0], args.class_names))

# The first 9 classes get keyboard shortcuts from 1-9
classes = OrderedDict()
classes = {args.class_names[x]:x+1 for x in range(len(args.class_names))}

# Here we define our HTML elements.
class Button():
    def __init__(self, btn_label) -> None:
        self.btn_label = btn_label
    def get_html(self):
        return '<a id="malignant" class="btn btn-lg btn-danger" role="button" style="width: 100px">%s</a>' % self.btn_label

class TaggerPage():
    def __init__(self, buttons) -> None:
        self.buttons = buttons
    def get_html(self):
        return """
        <!doctype html>

        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Labeller</title>
        <meta name="description" content="A web app for labelling images.">
        <meta name="Labeller">

        </head>

        <body>
        %s
        </body>
        </html>
        """ % " ".join(self.buttons)

# Create a database using the class labels provided
os.makedirs(os.path.join('.', 'db'), exist_ok=True)
conn = sqlite3.connect(os.path.join('.', 'db', 'tags.db'))
conn.execute('CREATE TABLE IF NOT EXISTS Tags (id INTEGER PRIMARY KEY, image STRING, label INTEGER, label_string STRING)')
conn.close()

print(TaggerPage([Button(btn_label='Label 1').get_html(), Button(btn_label='Label 2').get_html()]).get_html())

t = Tagger()
print(t.get_html())

f = Footer()
print(f.get_html())

# Opening a file that is distributed with the app can be done with pkg_resoruces
