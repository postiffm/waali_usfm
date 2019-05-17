from model import *
from sugar import *

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
			verse_lookup[current_chapter][item.number] = item
		if isinstance(item, FootNote):
			try:
				# remove the "try" once the issue with getting the chapters of Psalms resolved.
				verse = verse_lookup[item.chapter_num][item.verse_num]
				verse.text = verse.text.replace('*', f'\\f + \\fr {item.chapter_num}:{item.verse_num} {item.text} \\f*', 1)
			except Exception as e:
				pass
	return bible_items

	#todo: make sure to handle range footnotes. e.g. 45:10-11 

def process(bible_items):
	return pipe(bible_items, add_chapter_1_to_single_chapter_books, hook_up_footnotes)