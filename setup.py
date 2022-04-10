#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setup

@Author: Paul Hempel
@Date:   10.04.2022
"""
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="observables",
    version="0.0.1",
    author="Paul Hempel",
    author_email="paul.hempel@gmail.com",
    description="A package to use observable data",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/MetFred/python.observables",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)