#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:30:31 2020

@author: lidor
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TSC", # Replace with your own username
    version="0.0.1",
    author="Lidor Spivak",
    author_email="lidors15@gmail.com",
    description="Trash Spike classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lidors/TSC.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
