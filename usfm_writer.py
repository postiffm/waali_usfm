import os
from model import *

def write(bible_items):
	printable_items = get_printable_items(bible_items)

	usfm_dir = '../usfm_out_rev2'

	if not os.path.exists(usfm_dir):
		os.mkdir(usfm_dir)

	f = None
	for item in printable_items:
		if isinstance(item, Book):
			if f:
				f.close()
			f = open(usfm_dir + '/' + book_info[item.name]['file_name'], 'w')
		f.write(str(item) + '\n')
	f.close()
