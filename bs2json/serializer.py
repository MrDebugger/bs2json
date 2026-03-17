from typing import Iterable, Iterator, List, Dict, Union
from bs4 import element as Element, BeautifulSoup

from .models import ConversionConfig


class Serializer:
    """Stateless recursive engine that converts bs4 elements to JSON-compatible structures.

    Takes a ConversionConfig reference. Has no side effects — just config + element in,
    dict/list/string out.
    """

    def __init__(self, config: ConversionConfig):
        self.config = config

    def to_json(self, element: Union[Element.Tag, Iterator, Iterable], /) -> Union[Dict, List, str]:
        """Convert a BeautifulSoup element to JSON format.

        Args:
            element: The BeautifulSoup element to convert. Can be a single tag,
                or an Iterable/Iterator of multiple tags.

        Returns:
            JSON representation as a dict, list, or string.
        """
        json = {}
        text_name = self.config.text_name
        comment_name = self.config.comment_name

        if isinstance(element, Element.Tag):
            json[element.name] = self._tag(element)
            if (isinstance(json[element.name], dict) and
                json[element.name].get(text_name) and
                len(json[element.name]) == 1):
                return json[element.name][text_name]
            if (isinstance(json[element.name], list) and
                len(json[element.name]) == 1 and
                isinstance(json[element.name][0], dict) and
                json[element.name][0].get(text_name) and
                len(json[element.name][0]) == 1):
                return json[element.name][0][text_name]
            json = json[element.name]
        elif isinstance(element, Element.Comment) and self.config.include_comments:
            return element.output_ready()
        elif isinstance(element, Element.Comment):
            return None
        elif isinstance(element, Element.NavigableString):
            text = element.output_ready()
            if self.config.strip:
                text = text.strip()
            return text if text else None
        elif isinstance(element, BeautifulSoup):
            json = self.to_json(next(element.children))
        elif isinstance(element, Element.Doctype):
            json['doctype'] = str(element)
            json.update(self.to_json(element.next_element))
        elif isinstance(element, (Iterator, Iterable)):
            if self.config.keep_order:
                ordered_list = []
                for elem in element:
                    name = self._get_name(elem)
                    value = self.to_json(elem) or None
                    if not value and name in (text_name, comment_name):
                        continue
                    ordered_list.append({name: value})
                return ordered_list
            else:
                for elem in element:
                    name = self._get_name(elem)
                    value = self.to_json(elem) or None
                    if not value and name in (text_name, comment_name):
                        continue
                    if name in json:
                        json[name].append(value)
                    else:
                        json[name] = [value]
                self._fix(json)
        return json

    def _tag(self, element):
        """Process a single Tag element with its attributes and children."""
        attr_name = self.config.attr_name
        text_name = self.config.text_name
        json = {element.name: {}}
        if element.attrs:
            json[element.name][attr_name] = element.attrs
        if element.children:
            value = self.to_json(element.children)
            if isinstance(value, dict):
                json[element.name].update(value)
            elif isinstance(value, list):
                if element.attrs:
                    value.append(json[element.name])
                json[element.name] = value
            else:
                json[element.name] = value
        return json[element.name]

    def _fix(self, json):
        """Post-process grouped children: unwrap single-element lists, extract inline text."""
        text_name = self.config.text_name
        for element_name, value in json.items():
            if len(value) == 0:
                json[element_name] = None
            elif len(value) == 1:
                json[element_name] = value[0] or None
            else:
                items = filter(
                    lambda item: (
                        isinstance(item, dict)
                        and item.get(text_name)
                        and len(item) == 1
                    ),
                    value
                )
                for item in items:
                    index = value.index(item)
                    text = item.pop(text_name)
                    if not item:
                        del value[index]
                    value.insert(index, text)

    def _get_name(self, element):
        """Return the label name for a bs4 element (tag name, text label, or comment label)."""
        if isinstance(element, Element.Comment):
            name = self.config.comment_name
        elif isinstance(element, Element.NavigableString):
            name = self.config.text_name
        else:
            name = element.name
        return name
