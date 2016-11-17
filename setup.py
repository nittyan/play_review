# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='google_play_review_collector',
    version=0.8,
    author='hiroaki.nishi',
    author_email='kaziotore@gmail.com',
    url='https://github.com/nittyan/play_review',
    description='This script gathers reviews of Google Play.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    requires=['requests', 'beautifulsoup4']
)