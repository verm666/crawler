# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import crawler

setup(name='Crawler',
      version=crawler.__version__,
      description='HTTP Crawler',
      author=crawler.__author__,
      author_email=crawler.__author_email__,
      packages=[
          'crawler',
      ],
      scripts=[
          'bin/crawler'
      ]
)
