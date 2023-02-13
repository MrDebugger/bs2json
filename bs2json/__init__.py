#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .bs2json import BS2Json
from bs4 import element, BeautifulSoup

# deprecated version compatibility
bs2json = BS2Json
bs2json.convertAll = bs2json.convert_all
bs2json.toJson = bs2json.to_json

# extension to every tag element
def to_json(
        tag: element.Tag,
        include_comments: bool=True,
        strip: bool=True,
        attr_name: str="attrs",
        text_name: str="text",
        comment_name: str="comment",
    ):

    name_kwargs = dict(
        attr_name=attr_name,
        text_name=text_name,
        comment_name=comment_name
    )

    kwargs = dict(
        **name_kwargs,
        include_comments=include_comments,
        strip=strip
    )


    if not len(tag):
        return {}
    if isinstance(tag, BeautifulSoup):
        tag = tag.html or next(tag.children)
    if isinstance(tag, element.Doctype):
        json = {
            "doctype": str(tag)
        }
        json.update(tag.next_element.to_json(**kwargs))
        return json
    return bs2json(tag, **kwargs).convert()

def install():
    if not hasattr(element.Tag, 'to_json'):
        element.Tag.to_json = to_json

def remove():
    if hasattr(element.Tag, 'to_json'):
        del element.Tag.to_json