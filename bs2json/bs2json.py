from bs4 import ResultSet,element as Element

class bs2json:
	def __init__(self):
		self.__labels = {}
		self.labels(attributes='attributes',text='text')

	def labels(self,**kwargs):
		for k,w in kwargs.items():
			self.__labels[k] = w

	def convert(self,element,json=None):
		if not json:
			json ={}
		if not type(json) == dict:
			raise TypeError(f"convertAll(x,y) `y` argument must be a {dict.__name__} not {type(json).__name__}")
		if type(element) == Element.Tag:
			json[element.name] = self.toJson(element)
			return json
		else:
			raise TypeError(f"convert(x,y) `x` argument must be a {Element.__name__} not {type(element).__name__}")

	def convertAll(self,elements,List=None,join=False):
		if not List:
			List = []
		if not type(List) == list:
			raise TypeError(f"convertAll(x,y) `y` argument must be a {list} not {type(List).__name__}")
		if type(elements) == ResultSet:
			json = {}
			for element in elements:
				if join:
					if json.get(element.name):
						json[element.name].append(self.toJson(element))
					else:
						json[element.name] = [self.toJson(element)]
				else:
					List.append({element.name:self.toJson(element)})
			return List+[json] if join else List  
		else:
			raise TypeError(f"convertAll(x,y) `x` argument must be a {ResultSet.__name__} not {type(elements).__name__}")

	def toJson(self,element=None):
		json = {}
		if type(element) == Element.Tag:
			json[element.name] = {}
			if element.contents:
				json[element.name] = self.toJson(element.contents)
			elif element.string or element.text:
				json[element.name] = {self.__labels['text']:element.text or element.string}
			json[element.name][self.__labels['attributes']]= element.attrs
			return json[element.name]
		elif type(element)==list:
			elements = []
			text = ''
			for elem in element:
				if type(elem) == Element.Tag:
					value = self.toJson(elem)
					elements.append({elem.name:value})
				elif elem.strip():
					text += elem.strip()
			if text:
				json[self.__labels['text']] = text
			keys = [
						key 
						for elem in elements 
						for key in elem.keys()
					]
			for key in set(keys):
				values = []
				for elem in elements:
					for Key,value in elem.items():
						if Key == key:
							if value:
								values.append(value)
				if len(values) == 1:
					json[key] = values[0]
					continue
				if values:				
					json[key] = values
			return json
		else:
			return json
