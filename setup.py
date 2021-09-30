#!/usr/bin/env python

from setuptools import setup
import os

with open('PyPI.md') as f:
    long_description = f.read()

setup(name='labeller',
        packages=['labeller'],
        version='0.1.2',
        description='Create image labelling software for machine learning applications.',
        long_description=long_description,
        long_description_content_type='text/markdown',
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
