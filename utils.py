import re
from sugar import *
from model import *
from book_info import *

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

def child_count(elem):
	return len(elem.getchildren())


def is_int(s):
	try:
		if s == None:
			return False
		int(s)
		return True
	except ValueError:
		return False

def has_heading_style(elem):
	return has_style(elem, {'T5', 'P215', 'P216', 'P217', 'P218', 'P219', 'P221', 'P220', 'P272', 'P273', 'P379'})

def starts_with_verse_num(text):
	x = re.search('^\\s*\\d+($|[^:\\d])', text)
	return x != None

def get_verse_num(text):
	x = re.search('^\\s*(?P<num>\\d+)', text)
	return None if x == None else int(x.group('num'))

def has_chapter_or_chapter_header_pattern(bible_items):
	if len(bible_items) < 2:
		return False
	bible_items_last_index = len(bible_items) - 1;
	return isinstance(last(bible_items), Chapter) or (isinstance(bible_items[bible_items_last_index], Heading) and isinstance(bible_items[bible_items_last_index - 1], Chapter))

def has_style(elem, styles):
	for attribName, attribVal in elem.attrib.items():
		if attribName.endswith('style-name') and (attribVal in styles):
			return True
	return False

def normalize_space(text):
	r = re.compile(r'(\s+)')
	return r.sub(' ', text)

def is_white_space(text):
	return text == None or text == '' or text.isspace()

def concat_lines(line1, line2):
	return line1.strip() + ' ' + line2.strip()

def last_printable_item_is(bible_items, item_type):
	last_printable = last_printable_item(bible_items)
	return last_printable != None and isinstance(last_printable, item_type)

def last_printable_item(bible_items):
	for item in reversed(bible_items):
		if isinstance(item, Printable):
			return item
	return None

def is_page_header(text):
	if text == None:
		return False
	x = re.search('^(?P<book_name>[\'a-zA-Z\\s]+)[\\d-]+', text)
	return x != None and x.group('book_name').strip() in book_info.book_name_set


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
	return normalize_space(' '.join([t for t in elem.itertext()][1:]))


def is_parallel_passage_ref(elem_text):
	return get_parallel_passage_ref(elem_text) != None

def get_parallel_passage_ref(elem_text):
	m = re.match(r"^\(\s*(['\w\s]+G\.\s*\d+:\d+(-\d+)?\s*;?)+\s*\)$", elem_text)
	return m and m.string
