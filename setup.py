#! /usr/bin/env python3

from setuptools import setup

url = "https://github.com/MrDebugger/bs2json"
version = "0.0.2"

setup(
    name="bs2json",

    packages=["bs2json"],

    url=url,

    version=version,

    license="MIT",

    author="Ijaz Ur Rahim",
    author_email="ijazkhan095@gmail.com",

    description="Convert bs4 Tags into Json",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    keywords=[
        "parser",
        "html",
        "bs4",
        "BeautifulSoup",
        "soup",
        "bs4",
        "bs2json",
        "json"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],

    install_requires=[
        "bs4>=0.0.1"
    ]
)
