#!/usr/bin/env python

from setuptools import setup
import os

with open('PyPI.md') as f:
    long_description = f.read()

setup(name='labeller',
        packages=['labeller'],
        version='0.1.4',
        description='Create image labelling software for machine learning applications.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        author='Marcus D. Bloice',
        author_email='marcus.bloice@medunigraz.at',
        url='https://github.com/mdbloice/Labeller',
        classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ],
        install_requires=[
        'flask>=2.0',
        'flask-bootstrap>=3.3'
        ],
        # python_requires='>=3.5',
        # include_package_data=True,  # For the MANIFEST.in file...
        package_data={'': ['resources/*']}
        #scripts=['capitalize/bin/cap_script.py'],
    )
