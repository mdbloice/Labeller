#!/usr/bin/env python

from setuptools import setup
import os

with open('PYPI.md') as f:
    long_description = f.read()

setup(name='labeller',
        packages=['labeller'],
        version='0.1',
        description='Create image labelling software for machine learning applications.',
        license='MIT',
        author='Marcus D. Bloice',
        author_email='marcus.bloice@medunigraz.at',
        url='https://github.com/mdbloice/Labeller',
        install_requires=[
        'flask>=2.0',
        'flask-bootstrap>=3.3'
        ],
        # include_package_data=True,  # For the MANIFEST.in file...
        package_data={'': ['resources/*']}
        #scripts=['capitalize/bin/cap_script.py'],
    )
