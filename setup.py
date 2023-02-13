#! /usr/bin/env python3

from setuptools import setup, find_packages

url = "https://github.com/MrDebugger/bs2json"
version = "0.1.2"

setup(
    name="bs2json",
    packages=find_packages(),
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
        "Programming Language :: Python :: 3",
    ],

    install_requires=[
        "bs4>=0.0.1"
    ]
)
