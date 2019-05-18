import xml.etree.ElementTree as ET

import book_info
import model_post_processor
import usfm_writer
import paragraph_processor

# https://ubsicap.github.io/usfm/

def parse(content_xml_file):
	bible_items = []
	book_name_set = book_info.get_book_name_set()

	depth = 0
	for event, elem in ET.iterparse(content_xml_file, events = ['end', 'start']):
		if event == 'start':
			depth += 1
		elif event == 'end':
			if elem.tag.endswith('}p') and depth == 4:
				paragraph_processor.process(book_name_set, bible_items, elem)
			depth -= 1
	return bible_items

def main():

	bible_items = model_post_processor.process(parse('../content.xml'))

	usfm_writer.write(bible_items)


if __name__ == "__main__":
	main()
