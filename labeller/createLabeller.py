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
import pickle

# Internal imports
from labeller.htmlElements import Footer, Navbar, Index

parser = argparse.ArgumentParser(description='Generate an image labelling \
    application.', prog='python -m labeller')
parser.add_argument('class_names', metavar='class_names', nargs='+',
    help='a list of class names seperated by spaces')

args = parser.parse_args()

# Get the number of classes provided
n_classes = len(args.class_names)

if n_classes <= 1:
    print('Minimum number of classes is 2, you provided %s: %s' % (n_classes,
        args.class_names))
    sys.exit(1)

# Arguments look good.
print("Attempting to generate application with %s classes: %s." % (n_classes,
    ', '.join(args.class_names)))

extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]

im_dir = os.path.join('static', 'images')

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

# Create a config file as a pickle that we read later when the app is run.
# Not currently required.
#with open(os.path.join('.', 'labeller.pkl'), 'wb') as to_write:
#    pickle.dump(args.class_names, to_write)

# The first 9 classes get keyboard shortcuts from 1-9
# Do this in the appropriate class in htmlElements.py
#classes = OrderedDict()
#classes = {args.class_names[x]:x+1 for x in range(len(args.class_names))}

# Create a database using the class labels provided
os.makedirs(os.path.join('.', 'db'), exist_ok=True)
conn = sqlite3.connect(os.path.join('.', 'db', 'labels.db'))
conn.execute('CREATE TABLE IF NOT EXISTS labels (id INTEGER PRIMARY KEY, image STRING, label INTEGER, label_string STRING)')

# Search for images that have already been labelled:

already_labelled = 0

# This needs to be checked carefully for compatibility with Windows OSes
# due to paths and path seperators.
for image_path in image_paths:
    im = str.split(image_path, os.path.join("static", "images", os.sep))[-1]
    cursor = conn.cursor()
    res = cursor.execute('SELECT EXISTS(SELECT 1 FROM labels WHERE image="%s" LIMIT 1);' % im)
    data=cursor.fetchall()
    if data[0][0]:
        already_labelled += 1
    cursor.close()

print("%s images have already been labelled." % already_labelled)

# Insert some test data: Not required for release.
#cursor = conn.cursor()
#cursor.execute('INSERT INTO labels (image, label, label_string) VALUES("test.png", 0, "textlabel")')
#conn.commit()
#cursor.close()
conn.close()

print("Generating application with %s classes with the labels %s for %s images." % (n_classes, ', '.join(args.class_names), len(image_paths)))

# Create directory structure
os.makedirs(os.path.join('.', 'templates'), exist_ok=True)
os.makedirs(os.path.join('.', 'static', 'styles'), exist_ok=True)
# Places images in here for now, fix later using 'send_from_directory'
os.makedirs(os.path.join('.', 'static', 'images'), exist_ok=True)

# Use pkg_resources to open files or data installed with the package
app_py = pkg_resources.resource_string(__name__, os.path.join('resources', 'app.py'))
dashboard_css = pkg_resources.resource_string(__name__, os.path.join('resources', 'dashboard.css'))
about_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'about.html'))
labels_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'labels.html'))
navbar_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'navbar.html'))
favicon_ico = pkg_resources.resource_string(__name__, os.path.join('resources', 'favicon.ico'))
# index_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'index.html'))
# bootstrap_min_css = pkg_resources.resource_string(__name__, os.path.join('resources', 'bootstrap.min.css'))

# Copy any STATIC files to their appropriate directories here
with open(os.path.join('.', 'app.py'), 'wb') as to_write:
    to_write.write(app_py)

with open(os.path.join('.', 'static', 'styles', 'dashboard.css'), 'wb') as to_write:
    to_write.write(dashboard_css)

with open(os.path.join('.', 'static', 'favicon.ico'), 'wb') as to_write:
    to_write.write(favicon_ico)

with open(os.path.join('.', 'templates', 'about.html'), 'wb') as to_write:
    to_write.write(about_html)

with open(os.path.join('.', 'templates', 'labels.html'), 'wb') as to_write:
    to_write.write(labels_html)

with open(os.path.join('.', 'templates', 'navbar.html'), 'wb') as to_write:
    to_write.write(navbar_html)

# Currently CDNs are used for the Bootstrap CSS, but this may change in future
#with open(os.path.join('.', 'static', 'bootstrap.min.css'), 'wb') as to_write:
#    to_write.write(bootstrap_min_css)

# Create any DYNAMIC content here.
footer = Footer()
with open(os.path.join('.', 'templates', 'footer.html'), 'w') as to_write:
    to_write.write(footer.get_html())

index = Index(class_names=args.class_names)
with open(os.path.join('.', 'templates', 'index.html'), 'w') as to_write:
    to_write.write(index.get_html())

# Navbar currently is not dynamic content and can be copied from the static
# package resources
#navbar = Navbar()
#with open(os.path.join('.', 'templates', 'navbar.html'), 'w') as to_write:
#    to_write.write(navbar.get_html())

# See https://docs.python.org/3/library/__main__.html#module-__main__
# and https://docs.python.org/3/using/cmdline.html#cmdoption-m
# if __name__ == "__main__":
#     print("This is from labellerExec.py")
