
from model import *
from utils2 import *


def process(book_name_set, bible_items, elem):
	matching_patterns = [p for p in patterns if p.Matches(book_name_set, bible_items, elem)]
	if len(matching_patterns) != 1:
		print('uh oh')
	else:
		matching_patterns[0].Act(book_name_set, bible_items, elem)

class PatternBlank(object):
	def Matches(book_name_set, bible_items, elem):
		return get_text_rec(elem) == ''

	def Act(book_name_set, bible_items, elem):
		pass


class PatternBook(object):
	def Matches(book_name_set, bible_items, elem):
		return get_text_rec(elem) in book_name_set

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Book(get_text_rec(elem).strip(), elem))


patterns = [PatterBlank]