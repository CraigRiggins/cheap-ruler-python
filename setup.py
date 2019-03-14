#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='cheap-ruler-python',
      version='0.0.1',
      description='Python port of cheap ruler',
      author='Craig RIggins',
      author_email='criggins09@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE',
    )