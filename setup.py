#!/usr/bin/env python
""" configures the api package for control-gui """
from setuptools import setup, find_packages

setup(
    name="api",
    package_dir={"": "api/"},
    packages=find_packages(),
    scripts=["api/manage.py"],
)
