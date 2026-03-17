from typing import Iterable, Iterator, List, Dict, Union, Any, TextIO
from json import dump
from pprint import pprint
from bs4 import ResultSet, element as Element, BeautifulSoup

from .models import ConversionConfig
from .serializer import Serializer


class BS2Json:
    """Convert BeautifulSoup elements to JSON representation.

    Attributes:
        config (ConversionConfig): Conversion options and label names.
        soup (BeautifulSoup): Parsed HTML instance.
        last_obj: Result of the most recent conversion.
    """

    def __init__(self,
            soup: Union[Element.Tag, BeautifulSoup, str] = None,
            features: str = 'html.parser',
            *,
            include_comments: Union[bool, str] = True,
            strip: bool = True,
            keep_order: bool = False,
            **kwargs
        ) -> None:
        self.last_obj = {}
        self.soup = None

        attr_name = kwargs.pop("attr_name", "attrs")
        text_name = kwargs.pop("text_name", "text")
        comment_name = kwargs.pop("comment_name", "comment")

        self.config = ConversionConfig(
            attr_name=attr_name,
            text_name=text_name,
            comment_name=comment_name,
            include_comments=include_comments,
            strip=strip,
            keep_order=keep_order,
        )
        self._serializer = Serializer(self.config)

        if isinstance(soup, str):
            if (
                isinstance(features, str)
                and features in ['jsoup', 'lxml', 'html5lib', 'html.parser']
            ):
                kwargs['features'] = features
            else:
                kwargs['features'] = 'html.parser'
            self.soup = BeautifulSoup(soup, **kwargs)
        else:
            self.soup = soup

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def __repr__(self):
        tag = self.soup.name if self.soup else None
        return (
            f"BS2Json(tag={tag!r}, "
            f"include_comments={self.config.include_comments}, "
            f"strip={self.config.strip})"
        )

    def __call__(self, *args, **kwargs):
        return self.convert(*args, **kwargs)

    def save(self,
        file_obj: Union[str, TextIO] = 'bs2json-output.json',
        /,
        mode: str = 'w',
        encoding: str = 'utf-8',
        *,
        prettify: bool = True,
        indent: int = 4,
        **kwargs
    ):
        """Save the last converted object to a file."""
        if isinstance(file_obj, str):
            with open(file_obj, mode=mode, encoding=encoding, **kwargs) as file:
                dump(self.last_obj, file, indent=indent if prettify else 0)
        else:
            dump(self.last_obj, file_obj, indent=indent if prettify else 0)

    def prettify(self):
        """Print the prettified output of the last converted object."""
        pprint(self.last_obj)

    def labels(self, **kwargs) -> None:
        """Set label names for the JSON output.

        Args:
            attrs: Label for element attributes (default: "attrs")
            text: Label for text content (default: "text")
            comment: Label for comments (default: "comment")
        """
        field_map = {'attrs': 'attr_name', 'text': 'text_name', 'comment': 'comment_name'}
        for key, value in kwargs.items():
            if value is not None and key in field_map:
                setattr(self.config, field_map[key], value)

    def convert(self,
            element: Union[Element.Tag, str] = None,
            json: Dict = None,
            *,
            inplace: bool = False,
            **kwargs: Any
        ) -> Dict:
        """Convert a single bs4 tag or a tag matching the given string to a JSON object.

        Args:
            element: Tag to convert. If a string, finds a tag with that name in soup.
            json: Dictionary to update with the result.
            inplace: Whether to replace the soup object with the found tag.
            **kwargs: Passed to bs4.BeautifulSoup.find if element is a string.

        Returns:
            JSON representation of the element.
        """
        if (isinstance(element, str) or kwargs) and self.soup:
            element = self.soup.find(element, **kwargs)
        elif element is None and self.soup:
            element = self.soup

        if json is None:
            json = {}

        if not isinstance(json, dict):
            raise TypeError(
                "convertAll(x,y) `y` argument must be a "
                f"'dict' not {json.__class__.__name__!r}"
            )

        if element is None:
            self.last_obj = json
            return json

        if inplace:
            self.soup = element
        if isinstance(element, BeautifulSoup):
            element = element.html or next(element.children)
        elif isinstance(element, Element.Doctype):
            json['doctype'] = str(element)
            element = element.next_element
        if not isinstance(element, Element.Tag):
            raise TypeError(
                "convert(x,y) `x` argument must be"
                f" a 'Tag' not {element.__class__.__name__!r}"
            )

        json[element.name] = self._serializer.to_json(element)
        self.last_obj = json
        return json

    def convert_all(self,
            elements: Union[Element.Tag, str] = None,
            lst: List = None,
            *,
            join: bool = False,
            **kwargs
        ) -> List:
        """Convert multiple bs4 tags to a list of JSON objects.

        Args:
            elements: ResultSet of tags, or a string to find_all with.
            lst: List to append results to.
            join: If True, group results by tag name into a single dict.
            **kwargs: Passed to bs4.BeautifulSoup.find_all if elements is a string.

        Returns:
            List of dictionaries representing the tags.
        """
        if (isinstance(elements, str) or kwargs) and self.soup:
            elements = self.soup.find_all(elements, **kwargs)
        elif elements is None and self.soup:
            elements = self.soup.find_all(True)

        if not lst:
            lst = []

        if not isinstance(lst, list):
            raise TypeError(
                "convertAll(x, y) `y` argument must "
                f"be a 'list' not {lst.__class__.__name__!r}"
            )

        if elements is None:
            self.last_obj = lst
            return lst

        if not isinstance(elements, ResultSet):
            raise TypeError(
                "convertAll(x,y) `x` argument must be"
                f" 'ResultSet' not {elements.__class__.__name__!r}"
            )

        json = {}
        for element in elements:
            if join:
                if json.get(element.name):
                    json[element.name].append(self._serializer.to_json(element))
                else:
                    json[element.name] = [self._serializer.to_json(element)]
            else:
                lst.append({element.name: self._serializer.to_json(element)})
        if join:
            lst.append(json)
        self.last_obj = lst
        return lst
