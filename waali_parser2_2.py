import xml.etree.ElementTree as ET

import book_info
from model import *
from globals import *
from utils import *
import model_post_processor
import usfm_writer
import paragraph_processor

# https://ubsicap.github.io/usfm/

def main():
	global bible_items
	global book_name_set

	book_name_set = book_info.get_book_name_set()

	depth = 0
	for event, elem in ET.iterparse('../content.xml', events = ['end', 'start']):
		if event == 'start':
			depth += 1
		elif event == 'end':
			if elem.tag.endswith('}p') and depth == 4:
				paragraph_processor.process(book_name_set, bible_items, elem)
			depth -= 1

	bible_items = model_post_processor.process(bible_items)

	usfm_writer.write(bible_items)


if __name__ == "__main__":
	main()
