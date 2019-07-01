
bibles = []

class Bible:
	def __init__(self, name):
		self.name = name
		self.chapters = []

class Chapter:
	def __init__(self, number):
		self.number = number
		self.verses = []

class Verse:
	def __init__(self, number, text):
		self.number = number
		self.text = text

# load a model of every book, chapter, verse.
# if needed to facilitate the diff library, remove all newlines from every verse.
# Flag missing or extra books, chapters, verses.
# Flag verses that differ by more than x percent between the recovered version and the OCR version.
