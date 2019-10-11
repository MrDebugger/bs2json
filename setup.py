#! /usr/bin/env python3

from setuptools import setup

url = "https://github.com/MrDebugger/bs2json"
version = "0.0.0.1"

setup(
    name="bs2json",

    packages=["bs2json"],

    url=url,

    version=version,

    license="MIT",

    author="Ijaz Ur Rahim",
    author_email="ijazkhan095@gmail.com",

    description="Converter for bs4 Tags into Json",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    keywords=[
        "parser",
        "html",
        "bs4",
        "json"
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],

    install_requires=[
        "bs4>=0.0.1"
    ]
)
