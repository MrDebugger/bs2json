input_1 = """
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
    <p class="title">
        <b>The Dormouse's story</b>
    </p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
</body>
</html>
"""
expected_1 = {'html': {'head': {'title': "The Dormouse's story"}, 'body': {'p': [{'attrs': {'class': ['title']}, 'b': "The Dormouse's story"}, {'attrs': {'class': ['story']}, 'text': ['Once upon a time there were three little sisters; and their names were', ',', 'and', ';\n    and they lived at the bottom of a well.'], 'a': [{'attrs': {'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}, 'text': 'Elsie'}, {'attrs': {'href': 'http://example.com/lacie', 'class': ['sister'], 'id': 'link2'}, 'text': 'Lacie'}, {'attrs': {'href': 'http://example.com/tillie', 'class': ['sister'], 'id': 'link3'}, 'text': 'Tillie'}]}, {'attrs': {'class': ['story']}, 'text': '...'}]}}}
expected_2 = [{'a': {'attrs': {'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}, 'text': 'Elsie'}}, {'a': {'attrs': {'href': 'http://example.com/lacie', 'class': ['sister'], 'id': 'link2'}, 'text': 'Lacie'}}, {'a': {'attrs': {'href': 'http://example.com/tillie', 'class': ['sister'], 'id': 'link3'}, 'text': 'Tillie'}}]
expected_3 = [{'a': [{'attrs': {'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}, 'text': 'Elsie'}, {'attrs': {'href': 'http://example.com/lacie', 'class': ['sister'], 'id': 'link2'}, 'text': 'Lacie'}, {'attrs': {'href': 'http://example.com/tillie', 'class': ['sister'], 'id': 'link3'}, 'text': 'Tillie'}]}]
expected_4 = """{'html': {'body': {'p': [{'attrs': {'class': ['title']},\n                          'b': "The Dormouse's story"},\n                         {'a': [{'attrs': {'class': ['sister'],\n                                           'href': 'http://example.com/elsie',\n                                           'id': 'link1'},\n                                 'text': 'Elsie'},\n                                {'attrs': {'class': ['sister'],\n                                           'href': 'http://example.com/lacie',\n                                           'id': 'link2'},\n                                 'text': 'Lacie'},\n                                {'attrs': {'class': ['sister'],\n                                           'href': 'http://example.com/tillie',\n                                           'id': 'link3'},\n                                 'text': 'Tillie'}],\n                          'attrs': {'class': ['story']},\n                          'text': ['Once upon a time there were three little '\n                                   'sisters; and their names were',\n                                   ',',\n                                   'and',\n                                   ';\\n'\n                                   '    and they lived at the bottom of a '\n                                   'well.']},\n                         {'attrs': {'class': ['story']}, 'text': '...'}]},\n          'head': {'title': "The Dormouse's story"}}}\n"""