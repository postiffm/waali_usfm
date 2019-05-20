import os
from model import *
from book_info import books

def write(bible_items):
	printable_items = [item for item in bible_items if isinstance(item, Printable)]

	usfm_dir = '../usfm_out_rev2'

	if not os.path.exists(usfm_dir):
		os.mkdir(usfm_dir)

	f = None
	for item in printable_items:
		if isinstance(item, Book):
			if f:
				f.close()
			f = open(usfm_dir + '/' + books[item.name]['file_name'], 'w')
		f.write(str(item) + '\n')
	f.close()
