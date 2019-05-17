
import re
from model import *
from book_info import book_info
from globals import *

def is_int(s):
	try:
		if s == None:
			return False
		int(s)
		return True
	except ValueError:
		return False

def get_book_names():
	return list(book_info.keys())

def has_style(elem, styles):
	for attribName, attribVal in elem.attrib.items():
		if attribName.endswith('style-name') and (attribVal in styles):
			return True
	return False

def last(mylist):
	return mylist[len(mylist) - 1]

def starts_with_verse_num(text):
	x = re.search('^\\s*\\d+($|[^:\\d])', text)
	return x != None

def get_verse_num(text):
	x = re.search('^\\s*(?P<num>\\d+)', text)
	return None if x == None else int(x.group('num'))

def is_page_header(text):
	if text == None:
		return False
	x = re.search('^(?P<book_name>[\'a-zA-Z\\s]+)[\\d-]+', text)
	return x != None and x.group('book_name').strip() in book_name_set

def starts_with_footnote_ref(text):
	x = re.search('^\\d+:\\d+', text)
	return x != None

def get_footnote_ref(text):
	x = re.search('^(?P<ref>\\d+:\\d+)', text)
	if x == None:
		return None, None
	split = x.group('ref').split(':')
	return int(split[0]), int(split[1])

def get_footnote_text(elem):
	return ' '.join([t for t in elem.itertext()][1:])

def is_psalm_num(elem_text):
	if elem_text == None:
		return False
	return re.search("'Yienii\\s+\\d+", elem_text)

def get_psalm_num(elem_text):
	return int(re.search("'Yienii\\s+(?P<chapter>\\d+)", elem_text).group('chapter'))

def get_text_rec(elem):
	parts = []
	if elem.text:
		parts.append(elem.text)
	for item in elem:
		if item.text:
			parts.append(item.text)
		if item.tail:
			parts.append(item.tail)
	return ''.join(parts)

def has_verse_footnote_pageheader_pattern():
	if len(bible_items) < 3:
		return False
	bible_items_last_index = len(bible_items) - 1;
	return isinstance(bible_items[bible_items_last_index], PageHeader) and isinstance(bible_items[bible_items_last_index - 1], FootNote) and isinstance(bible_items[bible_items_last_index - 2], Verse)

def has_verse_pageheader_pattern():
	if len(bible_items) < 2:
		return False
	bible_items_last_index = len(bible_items) - 1;
	return isinstance(bible_items[bible_items_last_index], PageHeader) and isinstance(bible_items[bible_items_last_index - 1], Verse)

def has_verse_to_continue_before_page_break():
	return get_verse_before_page_break() != None

def get_verse_before_page_break():
	found_page_break = False
	for item in reversed(bible_items):
		if isinstance(item, PageHeader) or isinstance(item, FootNote):
			found_page_break = True
		elif isinstance(item, Verse) and found_page_break:
			return item
		else:
			return None

def has_chapter_or_chapter_header_pattern():
	if len(bible_items) < 2:
		return False
	bible_items_last_index = len(bible_items) - 1;
	return isinstance(last(bible_items), Chapter) or (isinstance(bible_items[bible_items_last_index], Heading) and isinstance(bible_items[bible_items_last_index - 1], Chapter))

def is_parent_of_last_bible_item(elem):
	return last(bible_items).elem in elem.getchildren()

def is_parallel_passage_ref(elem_text):
	return get_parallel_passage_ref(elem_text) != None

def get_parallel_passage_ref(elem_text):
	m = re.search(r"\(\s*(['\w\s]+G\.\s*\d+:\d+(-\d+)?\s*;?)+\s*\)", elem_text) 
	return m and m.string

def has_heading_style(elem):
	return has_style(elem, {'T5', 'P215', 'P216', 'P217', 'P218', 'P219', 'P221', 'P220', 'P272', 'P273', 'P379'})

def concat_lines(line1, line2):
	return line1.strip() + ' ' + line2.strip()
