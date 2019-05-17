import xml.etree.ElementTree as ET

from book_info import book_info
from model import *
from globals import *
from utils import *
import model_post_processor
import usfm_writer

# https://ubsicap.github.io/usfm/

def main():
	global bible_items
	global book_name_set

	book_names = get_book_names()

	for bn in book_names:
		book_name_set.add(bn.strip())

	prefix = None
	skip = False


	for event, elem in ET.iterparse('../content.xml', events = ['end', 'start']):
		if event == 'start':
			# todo: look for start of text element
			pass
		elif event == 'end':
			pass
			# todo: handle paragraphs under the text element

	bible_items = model_post_processor.process(bible_items)

	usfm_writer.write(bible_items)


if __name__ == "__main__":
	main()
