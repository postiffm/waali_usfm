import os
import re

class Book:
	def __init__(self, name):
		self.name = name
		self.chapters = {}

class Chapter:
	def __init__(self, number):
		self.number = number
		self.verses = {}

class Verse:
	def __init__(self, number, text):
		self.number = number
		self.text = text

def get_starting_number(text):
	x = re.search('^(?P<num>\\d+)', text)
	number_string = x.group('num')
	number = int(number_string)
	return number

def load_book(file_provider):
	book = None
	current_chapter = None
	current_verse = None
	for line in [l for l in file_provider.load_lines() if not l.isspace() and l != '']:
		#print('line:' + line + ':')
		tag = line[1]
		text = line[3:]
		#print('text:' + text + ':')
		if tag == 'h':
			book = Book(text)
		elif tag == 'c':
			number = get_starting_number(text)
			current_chapter = Chapter(number)
			book.chapters[number] = current_chapter
		elif tag == 'v':
			number = get_starting_number(text)
			text = text[len(str(number)) + 1:]
			current_verse = Verse(number, text)
			current_chapter.verses[number] = current_verse
		elif current_verse and (tag == 'q' or tag == 'p'):
			current_verse.text = current_verse.text + ' ' + text
	return book

def load_bible(files_provider):
	bible = {}
	for f in files_provider.list_files():
		book = load_book(f)
		bible[book.name] = book
	return bible

class FilesProvider:
	def __init__(self, directory):
		self.directory = directory

	def list_files(self):
		return [FileProvider(os.path.join(self.directory, f)) for f in os.listdir(self.directory)]

class FileProvider:
	def __init__(self, path):
		self.path = path

	def load_lines(self):
		with open(self.path, 'r') as f:
			return f.readlines()

def diff_subtract_chapter(minuend, subtrahend, subtrahend_name):
	missing = []
	for verse in minuend.verses:
		if not verse in subtrahend.verses:
			missing.append(f'verse {verse} missing from {subtrahend_name}')

	return missing

def diff_subtract_book(minuend, subtrahend, subtrahend_name):
	missing = []
	#print(minuend)
	for chapter in minuend.chapters:
		if not chapter in subtrahend.chapters:
			missing.append(f'chapter {chapter} missing from {subtrahend_name}')
		else:
			missing = missing + diff_subtract_chapter(minuend.chapters[chapter], subtrahend.chapters[chapter], subtrahend_name + "." + str(chapter))
	return missing

def diff_subtract_bible(minuend, subtrahend, subtrahend_name):
	missing = []

	for book_name in minuend:
		if not book_name in subtrahend:
			missing.append(f'book {book_name} misisng from {subtrahend_name}.')
		else:
			#print(minuend[book_name])
			missing = missing + diff_subtract_book(minuend[book_name], subtrahend[book_name], subtrahend_name + "." + book_name)
	return missing

def main():
	# load a model of every book, chapter, verse.
	ocr_bible = load_bible(FilesProvider('../usfm_ocr_modified_for_compare'))
	recovered_bible = load_bible(FilesProvider('../usfm_out_rev2'))

	missing = diff_subtract_bible(ocr_bible, recovered_bible, "RecoverdBible")

	print("\n".join(missing))

	# if needed to facilitate the diff library, remove all newlines from every verse.
	# Flag missing or extra books, chapters, verses.
	# Flag verses that differ by more than x percent between the recovered version and the OCR version.

if __name__ == "__main__":
	main()
