# labellerExec.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.
import argparse
import sys
import sqlite3
import os
from collections import OrderedDict
import glob
import pkg_resources

# Internal imports
from labeller.htmlElements import Footer, Tagger

parser = argparse.ArgumentParser(description='Generate an image labelling application.', prog='python -m labeller')
# No need to actually pass the number of classes, we just get that from the number of class names
# parser.add_argument('n_classes', metavar='n_classes', type=int, nargs=1, help='the number of classes')
parser.add_argument('class_names', metavar='class_names', nargs='+', help='a list of class names seperated by spaces')
args = parser.parse_args()

# Get the number of classes provided
n_classes = len(args.class_names)

if n_classes <= 1:
    print('Minimum number of classes is 2, you provided %s: %s' % (n_classes, args.class_names))
    sys.exit(1)

#if n_classes != len(args.class_names):
#    print('Number of classes (%s) does equal number of class names provided (%s)' % (n_classes[0], len(args.class_names)))
#    sys.exit(1)

extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]

im_dir = 'images'

if not os.path.exists(os.path.join('.', im_dir)):
    print("No directory named '%s' found in the current directory: %s). Aborting." % (im_dir, os.getcwd()))
    sys.exit(1)
else:
    print("Found a directory named %s: %s\nSearching for images with the following extensions: %s" % (im_dir, os.path.join(os.getcwd(), im_dir), ' '.join(extensions)))

image_paths = []
for ext in extensions:
    image_paths.extend(glob.glob(os.path.join('.', im_dir, ext)))

if len(image_paths) <= 0:
    print("No images found in %s. Aborting." % os.path.join(os.getcwd(), im_dir))
    sys.exit(1)
else:
    print("Found %s images in %s" %(len(image_paths), os.path.join(os.getcwd(), im_dir)))
    print(image_paths)

print("Generating application with %s classes with the labels: %s." % (n_classes, ', '.join(args.class_names)))

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

#print(TaggerPage([Button(btn_label='Label 1').get_html(), Button(btn_label='Label 2').get_html()]).get_html())

t = Tagger()
#print(t.get_html())

f = Footer()
#print(f.get_html())

# Create a database using the class labels provided
os.makedirs(os.path.join('.', 'db'), exist_ok=True)
conn = sqlite3.connect(os.path.join('.', 'db', 'tags.db'))
conn.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, image STRING, label INTEGER, label_string STRING)')
conn.close()

# Use pkg_resources to open files or data installed with the package
app_py = pkg_resources.resource_string(__name__, os.path.join('resources', 'app.py'))

# Copy to the current directory
with open('app.py', 'wb') as f:
    f.write(app_py)


# See https://docs.python.org/3/library/__main__.html#module-__main__
# and https://docs.python.org/3/using/cmdline.html#cmdoption-m
# if __name__ == "__main__":
#     print("This is from labellerExec.py")
