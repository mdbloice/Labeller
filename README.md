![Labeller-Logo](https://github.com/mdbloice/AugmentorFiles/blob/master/Labeller/Labeller-Logo.png)

Quickly set up an image labelling web application for the tagging of images by humans for supervised machine learning tasks.

## Introduction

*Labeller* allows you to quickly set up an image tagging web application for labelling of images.

## Usage

1. Install _Labeller_ using `pip install labeller` from the command line
2. Run `python -m labeller class_1 class_2 ... class_n` in a directory containing your images in a subdirectory named `images`, where `class_1 class_2 ... class_n` is a list of your class names separated by spaces.
3. Run `python -m flask run` to start the web application.

Example:

```bash
$ python -m labeller car tree bike house
$ python -m flask run
```
See the [Options](#options) section for configuration options.

Run `python -m labeller` without any arguments for help.

## How Labeller Works
When you create a new labelling application, _Labeller_ will generate a web application based on the number of classes you have defined during initialisation. Images stored in `images` will be displayed randomly to the user, and they can be labelled with one of the classes provided during the app initialisation.

The built application will have the following structure:

```
.
├── app.py
├── db
│   └── tags.db
├── images
│   ├── im_1.png
│   ├── im_2.png
│   ├── ...
│   └── im_n.png
├── static
│   └── styles
│       └── dashboard.css
└── templates
    ├── about.html
    └── footer.html

```

## FAQ

- I want to clear the database and start labelling again
  - Delete the sqlite database in the `db` directory. The app will regenerate a new, empty database when run if no database exists.

## Options

Currently, the only user definable parameters is the list of class names. This will change as the application develops.

## Requirements

- Python >=3.5

The following Python packages are required, and will be downloaded automatically by `pip` during installation:

- `flask`
- `flask-bootstrap`

as well and their requirements.

## Known Issues

- HTML formatting of generated output needs work

## Future Work

- Consensus labelling (combining labelling efforts across users)
- Multi class labelling (labelling an image with more than 1 label)
- Free-text tagging/labelling
- API access for running instances to get image tags
- Docker image?
