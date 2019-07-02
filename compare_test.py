import os

class 

class Book:
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
def load_book(path):
	book = None
	current_chapter = None
	current_verse = None
	with open(path, 'r') as f:
		for line in [l.strip() for l in f.readlines()]:
			tag = line[1]
			text = line[5:0]
			if tag == 'h':
				book = Book(text)
			elif tag == 'c':
				number = int(text)
				current_chapter = Chapter(number)
				book.chapters[number] = current_chapter
			elif tag == 'v':
				x = re.search('^(?P<num>\\d+)', text)
				number_string = x.group('num')
				number = int(number_string)
				text = text[len(number_string) + 1:]
				current_verse = Verse(number, text)
			elif tag == 'q' or tag == 'p'
				current_verse.text = current_verse.text + ' ' + text
	return book

def load_bible(path):
	files = os.listdir(path)
	bible = []
	for f in files:
		book = load_book(os.path.join(path, f))
		bible[book.name] = book
	return bible

ocr_bible_path = '../usfm'
recovered_bible_path = '../usfm_out_rev2'

ocr_bible = load_bible(ocr_bible_path)
recovered_bible = load_bible(recovered_bible_path)

# if needed to facilitate the diff library, remove all newlines from every verse.
# Flag missing or extra books, chapters, verses.
# Flag verses that differ by more than x percent between the recovered version and the OCR version.
