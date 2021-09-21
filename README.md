# Labeller
Quickly set up an image labelling web application for the tagging of images by humans for supervised machine learning tasks.

## Introduction

*Labeller* allows you to quickly set up an image tagging web application for labelling of images. 

## Usage

1. Install _Labeller_ using `pip install labeller` from the command line
2. Run `python -m labeller class_1 class_2 ... class_n` in a directory containing your images in a subdirectory called `images` or `img`, where `class_1 class_2 ... class_n` is a list of your class names. This will create a new web application in the directory `build` 
3. Run `python -m flask run` to start the web application.

Example: 

```bash
$ python -m labeller car tree bike house
$ python -m flask run
```
See the [Options](#options) section for configuration options. 

Run `python -m labeller` without any arguments for help.

## How Labeller Works
When you create a new labelling application, _Labeller_ will generate a web application based on the number of classes you have defined. Images stored in `img` or `images` will be displayed to the user, and they can be labelled with one of the classes provided during the app initialisation.

## Options

Currently, the only options are to supply the number of classes and the class labels. This will change as the application develops.

## Requirements

The following packages are required, and will be downloaded automatically by `pip` during installation:

- flask
- flask-bootstrap

## Docker
Work in progress.
