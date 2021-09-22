#!/usr/bin/env python

from setuptools import setup

setup(name='labeller',
        version='0.1',
        # list folders, not files
        #packages=['capitalize',
        #          'capitalize.test'],
        #scripts=['capitalize/bin/cap_script.py'],
        include_package_data=True,
        package_data={'': ['style.css']},
    )