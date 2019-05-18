
from model import *
from utils import *


def process(book_name_set, bible_items, elem):
	matching_patterns = [p for p in patterns if p.Matches(book_name_set, bible_items, elem)]
	if len(matching_patterns) != 1:
		print('Expected 1 matching pattern but found: ' + str(len(matching_patterns)))
	else:
		matching_patterns[0].Act(book_name_set, bible_items, elem)

class PatternBlank(object):
	def Matches(book_name_set, bible_items, elem):
		return get_text_rec(elem).isspace()

	def Act(book_name_set, bible_items, elem):
		pass


class PatternBook(object):
	def Matches(book_name_set, bible_items, elem):
		return get_text_rec(elem) in book_name_set

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Book(get_text_rec(elem).strip(), elem))

class PatternChapter(object):
	def Matches(book_name_set, bible_items, elem):
		return is_int(get_text_rec(elem)) and child_count(elem) == 0

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Chapter(int(get_text_rec(elem)), elem))

class PatternFirstVerseWithoutNumber(object):
	def Matches(book_name_set, bible_items, elem):
		elem_text_rec = get_text_rec(elem)
		return not PatternBlank.Matches(book_name_set, bible_items, elem) and \
		    not has_heading_style(elem) and \
		    not starts_with_verse_num(elem_text_rec) and \
		    has_chapter_or_chapter_header_pattern(bible_items)

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Verse(1, get_text_rec(elem), elem))

class PatternVerseWithNumber(object):
	def Matches(book_name_set, bible_items, elem):
		return starts_with_verse_num(get_text_rec(elem)) and \
			not PatternChapter.Matches(book_name_set, bible_items, elem)

	def Act(book_name_set, bible_items, elem):
		elem_text_rec = get_text_rec(elem)
		verse_num = get_verse_num(elem_text_rec)
		verse_text = elem_text_rec[len(str(verse_num)):].strip()
		verse_text = normalize_space(verse_text)
		bible_items.append(Verse(verse_num, verse_text, elem))

patterns = [PatternBlank, PatternBook, PatternChapter,
	PatternFirstVerseWithoutNumber, PatternVerseWithNumber]