import xml.etree.ElementTree as ET

import book_info
import usfm_writer
import paragraph_processor
from model import *
from sugar import *
from utils import format_cross_ref

# https://ubsicap.github.io/usfm/

def parse(content_xml_file):
	bible_items = []
	book_name_set = book_info.book_name_set

	errors = []
	depth = 0
	for event, elem in ET.iterparse(content_xml_file, events = ['end', 'start']):
		if event == 'start':
			depth += 1
		elif event == 'end':
			if elem.tag.endswith('}p') and depth == 4:
				succeeded, error = paragraph_processor.process(book_name_set, bible_items, elem)
				if not succeeded:
					errors.append(error)
			depth -= 1
	return bible_items, errors

def add_chapter_1_to_single_chapter_books(bible_items):
	revised_bible_items = []
	expect_chapter_1 = False
	last_book = None
	for item in bible_items:
		if isinstance(item, Book):
			expect_chapter_1 = True
			last_book = item
		if isinstance(item, Chapter):
			expect_chapter_1 = False
		if isinstance(item, Verse) and expect_chapter_1:
			revised_bible_items.append(Chapter(1, None))
			expect_chapter_1 = False
		revised_bible_items.append(item)
	return revised_bible_items

def hook_up_footnotes(bible_items):
	verse_lookup = {}
	current_chapter = None

	for item in bible_items:
		if isinstance(item, Chapter):
			verse_lookup[item.number] = {}
			current_chapter = item.number
		if isinstance(item, Verse):
			if current_chapter != None:
				verse_lookup[current_chapter][item.number] = item
			# else we are probably running inside a test case where theres a verse without a chapter.
		if isinstance(item, FootNote):
			try:
				# remove the "try" once the issue with getting the chapters of Psalms resolved.
				verse = verse_lookup[item.chapter_num][item.verse_num]
				verse.text = verse.text.replace('*', f'\\f + \\fr {item.chapter_num}:{item.verse_num} {item.text} \\f*', 1)
			except Exception as e:
				pass
	return bible_items

def format_cross_references(bible_items):
	current_chapter = None
	for item in bible_items:
		if isinstance(item, Chapter):
			current_chapter = item.number
		if isinstance(item, Verse):
			item.text = format_cross_ref(item.text, f'{current_chapter}:{item.number}')
	return bible_items

	#todo: make sure to handle range footnotes. e.g. 45:10-11 

def extract_model(content_xml_file):
	bible_items, errors = parse(content_xml_file)
	bible_items = pipe(bible_items, add_chapter_1_to_single_chapter_books, hook_up_footnotes, format_cross_references)
	return bible_items, errors