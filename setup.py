from __future__ import with_statement

from setuptools import setup

import ec3

ec3_classifiers = [
    "Programming Language :: Python :: 3",
]

with open("README.md", "r") as file:
    ec3_long_description = file.read()

setup(name="ec3",
      version=ec3.__version__,
      author="Conor Anderson",
      author_email="conor@conr.ca",
      url="https://gitlab.com/ConorIA/ec3.py",
      py_modules=["ec3"],
      description="Access climate data from Government of Canada's Historical Climate Data API",
      long_description=ec3_long_description,
      license="GPL3",
      classifiers=ec3_classifiers,
      python_requires=">=3.6",
      )
