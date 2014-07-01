class Item(object):
	def __init__(self):
		self.id = ''
		self.path = ''
		self.thumb = ''
		self.title = ''
		self.has_children = False


	@classmethod
	def MapFromJson(self, json):
		item = Item()

		if json.get('id'):
			item.id = json.get('id')

		if json.get('url'):
			# changing the url so that it only returns the full eppisodes and no clips/extras
			item.path = json.get('url').replace('sbs-app-section-sbstv','sbs-app-section-programs')

		if json.get('thumbnail'):
			item.thumb = json.get('thumbnail')

		if json.get('name'):
			item.title = json.get('name')

		if json.get('children'):
			item.has_children = True

		return item
