from typing import Iterable, Iterator, List, Dict, Union, Any, NoReturn, TextIO
from json import dump, dumps
from pprint import pprint
from bs4 import ResultSet, element as Element, BeautifulSoup

class BS2Json:
    """Convert BeautifulSoup elements to JSON representation.

    Attributes:
        include_comments (bool): Whether to include comments in the JSON representation.
        strip (bool): Whether to remove whitespaces from the start and end of text.
        __labels (Dict): Dictionary of labels for converting BeautifulSoup elements to JSON.
        soup (BeautifulSoup): Instance of BeautifulSoup class.
    """
    include_comments = True
    strip = True
    __labels: Dict = {}
    soup: BeautifulSoup = None
    last_obj: Dict = {}

    def __init__(self,
            soup: Union[Element.Tag, BeautifulSoup, str]=None,
            features: str='html.parser',
            *,
            include_comments: Union[bool, str]=True,
            strip: bool=True,
            **kwargs
        ) -> NoReturn:
        """Initialize the instance of bs2json class.

        Args:
            soup (Union[Element.Tag, BeautifulSoup, str], optional): Instance of BeautifulSoup class
                or a string that can be converted to BeautifulSoup. Defaults to None.
            include_comments (bool, optional): Whether to include comments in the JSON
                representation. Defaults to True.
            strip (bool): Whether to remove whitespaces from the start and end of text.
            **kwargs: Keyword arguments for initializing BeautifulSoup.
        """

        attr_name = kwargs.pop("attr_name", "attrs")
        text_name = kwargs.pop("text_name","text")
        comment_name = kwargs.pop("comment_name","comment")

        if isinstance(soup, str):
            # incase someone provides the features value in BeautifulSoup as argument
            # to include_comments
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
        self.include_comments = include_comments
        self.strip = strip

        self.labels(attrs=attr_name, text=text_name, comment=comment_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def __call__(self, *args, **kwargs):
        return self.convert(*args, **kwargs)

    def save(self,
        file_obj: Union[str, TextIO]='bs2json-output.json',
        /,
        mode: str='w',
        encoding: str='utf-8',
        *,
        prettify: bool=True,
        indent: int=4,
        **kwargs
    ):
        """
            Saves the last converted object into a file
        """
        if isinstance(file_obj, str):
            with open(file_obj, mode=mode, encoding=encoding, **kwargs) as file:
                dump(self.last_obj, file , indent=indent if prettify else 0)
        else:
            dump(self.last_obj, file_obj, indent=indent if prettify else 0)


    def prettify(self):
        """
            Print the prettified output of the last converted object
        """
        pprint(self.last_obj)

    def labels(self, **kwargs)  -> NoReturn:
        """Set labels for converting BeautifulSoup elements to JSON.

        Args:
            **kwargs: Keyword arguments for setting labels.
        """

        for key, word in kwargs.items():
            if word is not None:
                self.__labels[key] = word

    def convert(self,
            element: Union[Element.Tag, str]=None,
            json: Dict=None,
            *,
            inplace: bool=False,
            **kwargs: Any
        ) -> Dict:
        """
        This method converts a single `bs4` tag or a tag matching the given string to a JSON object.

        Args:
            element (Union[Element.Tag, str], optional): The tag to be converted to a JSON object.
                If a string is given, the method will try to find a tag with the given name in
                the parsed soup.
            json (Dict, optional): A dictionary that will be updated with the resulting JSON object.
            inplace (Bool, optional): Wheter to replace the soup object with the found or
            provided tag.
            **kwargs: Additional arguments to be passed to `bs4.BeautifulSoup.find` method,
                if the `element` is a string.

        Returns:
            Dict: JSON representation of the element.
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

        json[element.name] = self.to_json(element)
        self.last_obj = json
        return json

    def convert_all(self,
            elements: Union[Element.Tag, str]=None,
            lst: List=None,
            *,
            join: bool=False,
            **kwargs
        ) -> List:
        """
        This method converts a list of `bs4` tags or tags matching the given string to a list
        of JSON objects.

        Args:
            elements (bs4.ResultSet or str): A ResultSet of `bs4` tags to be converted to a
                list of JSON objects. If a string is given, the method will try to find
                all the tags with the given name in the parsed soup.
            lst (list): A list that will be updated with the resulting list of JSON objects.
            join (bool): If set to `True`, the resulting list of JSON objects will be joined
                into a single JSON object, with the tag names as keys and the values as lists
                of JSON objects representing the respective tags.
            **kwargs: Additional arguments to be passed to `bs4.BeautifulSoup.find_all`
                method, if the `elements` is a string.

        Returns:
            list: A list of dictionaries representing the tags in a JSON format.
        """

        if (isinstance(elements, str) or kwargs) and self.soup:
            elements = self.soup.find_all(elements, **kwargs)
        elif elements is None and self.soup:
            elements = self.soup

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
                    json[element.name].append(self.to_json(element))
                else:
                    json[element.name] = [self.to_json(element)]
            else:
                lst.append({element.name:self.to_json(element)})
        if join:
            lst.append(json)
        self.last_obj = lst
        return lst

    def __fix(self, json):
        text_name = self.__labels['text']
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

    def __tag(self, element):
        attr_name = self.__labels['attrs']
        text_name = self.__labels['text']
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

    def __get_name(self, element):
        if isinstance(element, Element.Comment):
            name = self.__labels['comment']
        elif isinstance(element, Element.NavigableString):
            name = self.__labels['text']
        else:
            name = element.name
        return name

    def to_json(self,
            element: Union[Element.Tag, Iterator, Iterable], /
        ) -> Union[Dict, List, str]:
        """
        Convert BeautifulSoup element object to JSON format.

        Args:
            element (Union[Element.Tag, Iterator, Iterable]): The BeautifulSoup element to
                be converted to JSON format. Can be a single tag or an Iterable or Iterator
                of multiple tags.

        Returns:
            Union[Dict, List, str]: The JSON representation of the BeautifulSoup element,
                including tag names, tag attributes, tag text and/or comments.
        """
        json = {}
        text_name = self.__labels['text']
        comment_name = self.__labels['comment']
        if isinstance(element,Element.Tag):
            json[element.name] = self.__tag(element)
            if json[element.name].get(text_name) and len(json[element.name]) == 1:
                return json[element.name][text_name]
            json = json[element.name]
        elif isinstance(element, Element.Comment) and self.include_comments:
            return element.output_ready()
        elif isinstance(element, Element.NavigableString):
            text = element.output_ready()
            if self.strip:
                text = text.strip()
            return text if text else None
        elif isinstance(element, BeautifulSoup):
            json = self.to_json(next(element.children))
        elif isinstance(element, Element.Doctype):
            json['doctype'] = str(element)
            json.update(self.to_json(element.next_element))
        elif isinstance(element, (Iterator, Iterable)):
            for elem in element:
                name = self.__get_name(elem)
                value = self.to_json(elem) or None
                if not value and name == text_name:
                    continue
                if name in json:
                    json[name].append(value)
                else:
                    json[name] = [value]
            self.__fix(json)
        return json
