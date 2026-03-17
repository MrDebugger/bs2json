from bs4 import element, BeautifulSoup

from .converter import BS2Json


def to_json(
        tag: element.Tag,
        include_comments: bool = True,
        strip: bool = True,
        keep_order: bool = False,
        attr_name: str = "attrs",
        text_name: str = "text",
        comment_name: str = "comment",
    ):
    """Convert a bs4 Tag to JSON. Designed to be monkey-patched onto element.Tag."""
    kwargs = dict(
        attr_name=attr_name,
        text_name=text_name,
        comment_name=comment_name,
        include_comments=include_comments,
        strip=strip,
        keep_order=keep_order,
    )

    if not len(tag):
        return {}
    if isinstance(tag, BeautifulSoup):
        tag = tag.html or next(tag.children)
    if isinstance(tag, element.Doctype):
        json = {"doctype": str(tag)}
        json.update(tag.next_element.to_json(**kwargs))
        return json
    return BS2Json(tag, **kwargs).convert()


def install():
    """Add to_json() method to every bs4 Tag element."""
    if not hasattr(element.Tag, 'to_json'):
        element.Tag.to_json = to_json


def remove():
    """Remove the to_json() method from bs4 Tag elements."""
    if hasattr(element.Tag, 'to_json'):
        del element.Tag.to_json
