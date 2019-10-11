from bs4 import BeautifulSoup,ResultSet,element as Element

class bs2json:
	def convert(self,element,json={}):
		if not type(json) == dict:
			raise TypeError(f"convertAll(x,y) `y` argument must be a {dict.__name__} not {type(json).__name__}")
		if type(element) == Element.Tag:
			json[element.name] = self.toJson(element)
			return json
		else:
			raise TypeError(f"convert(x,y) `x` argument must be a {Element.__name__} not {type(element).__name__}")

	def convertAll(self,elements,List=[]):
		if not type(List) == list:
			raise TypeError(f"convertAll(x,y) `y` argument must be a {list.__name__} not {type(List).__name__}")
		if type(elements) == ResultSet:
			for element in elements:
				List.append(self.toJson(element))
			return List
		else:
			raise TypeError(f"convertAll(x,y) `x` argument must be a {ResultSet.__name__} not {type(elements).__name__}")

	def toJson(self,elem=None,json={}):
		if type(elem) == Element.Tag:
			json[elem.name] = {'attributes':elem.attrs}
			json[elem.name] = self.toJson(elem.contents,json[elem.name])
			return json[elem.name]
		elif len(elem):
			elements = []
			text = ''
			for el in elem:
				if type(el) == Element.Tag:
					value = self.toJson(el,json)
					elements.append({el.name:value})
				else:
					text += el.strip()
			json['text'] = text
			keys = [key for el in elements for key in el.keys()]
			for key in set(keys):
				values = []
				for el in elements:
					for Key,value in el.items():
						if Key == key:
							if value:
								values.append(value)
				if values:				
					json[key] = values
			return json
		else:
			return 
