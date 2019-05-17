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


	for event, elem in ET.iterparse('../content.xml', events = ['end']):

		elem_text = None
		if prefix != None and elem.tag.endswith('span') and str(elem.text) != None:
			elem_text = prefix + str(elem.text)
		else:
			elem_text = None if elem.text == None else str(elem.text)
		if elem_text != None and (elem_text.isspace() or elem_text == ''):
			elem_text = None
		prefix = None

		elem_text_rec = get_text_rec(elem)

		if elem_text == "'Luki Gbangu" and elem.tag.endswith('span'):
			#special handling for an anomolous page header
			skip = True
		elif skip:
			skip = False
		elif elem.tag.endswith('span') and elem_text == '\'':
			# Merge any ' span into the subsequent span. Fixes an anomoly with standalone ' chars.
			prefix = '\''
		elif elem_text_rec == '':
			# example: see context of <text:span text:style-name="T5">Eerong dankpali ang bohi</text:span>
			pass
		elif is_page_header(elem_text):
			# skip those pesky page headers like "'Munpiilee Gbangu 1-2" that are specific to the printed page format.
			bible_items.append(PageHeader(elem))
		elif (elem_text == None or elem_text == '') and len(elem.getchildren()) == 0:
		    # skip over empty elements, including paragraphs.
		    # Empty paragraphs seem too specific to the printed page format.
		    # todo: handle tabs instead of skipping
		    # todo: handled "<text:s/>" intead of skipping
			pass
		elif is_int(elem_text) and len(elem.getchildren()) == 0:
			bible_items.append(Chapter(int(elem_text), elem))
		elif is_psalm_num(elem_text) and len(elem.getchildren()) == 0:
			bible_items.append(Chapter(get_psalm_num(elem_text), elem))
		elif len(bible_items) > 0 and not elem_text_rec.isspace() and has_chapter_or_chapter_header_pattern() and not is_parent_of_last_bible_item(elem) and not has_heading_style(elem) and not starts_with_verse_num(elem_text_rec):
			#T5 is a style used for bold headers and for chapter numbers, so if style is T5, it isn't a verse.

			bible_items.append(Verse(1, elem_text_rec, elem))
		elif elem_text != None and elem_text.strip() in book_name_set and not has_style(elem, {'P227', 'T10'}):
			# most books are in a p element, but some like "Eesiter Gbangu" are in a span element.
			bible_items.append(Book(elem_text.strip(), elem))
		elif elem_text != None and has_heading_style(elem):
			# todo: double check this style list.
			# Note: Style T4 is also used for the first verse of a chapter. However, the first verse case
			# is alreay handled in a previous if condition.
			if isinstance(last(bible_items), Heading):
				last(bible_items).text = concat_lines(last(bible_items).text, elem_text)
			else:
				bible_items.append(Heading(elem_text, elem))
		elif elem.tag.endswith('}p') and starts_with_verse_num(elem_text_rec) and not is_parent_of_last_bible_item(elem):
			verse_num = get_verse_num(elem_text_rec)

			if verse_num == 1 and isinstance(last(bible_items), Verse):
				#woops. There can't be two verse 1's, so the previous thing was actually a heading, not a verse.
				#In the Psalms the there are headings that appear in between the chapter number and the first verse.
				heading_mistaken_for_verse_1 = bible_items.pop()
				
				bible_items.append(Heading(heading_mistaken_for_verse_1.text, elem))

			verse_text = elem_text_rec[len(str(verse_num)):].strip()
			bible_items.append(Verse(verse_num, verse_text, elem))
		elif elem_text != None and starts_with_footnote_ref(elem_text):
			footnote_chapter, footnote_verse = get_footnote_ref(elem_text)
			footnote_text = get_footnote_text(elem)
			bible_items.append(FootNote(footnote_chapter, footnote_verse, footnote_text, elem))
		elif elem_text_rec != '' and not elem_text_rec.startswith('*________') and elem.tag.endswith('}p') and len(bible_items) > 0 and (isinstance(last(bible_items), Verse) or isinstance(last(bible_items), FootNote)) and not last(bible_items).elem in elem.getchildren():
			# This is a continuation of a verse or footnote in a separate paragraph element.

			last(bible_items).text = concat_lines(last(bible_items).text, get_text_rec(elem))
		elif elem_text_rec != '' and elem.tag.endswith('}p') and len(bible_items) > 0 and has_verse_footnote_pageheader_pattern():
			# This is a continuation of a verse or footnote in a separate paragraph element.

			item = bible_items[len(bible_items) - 3]
			item.text = concat_lines(item.text, get_text_rec(elem))
		elif elem_text_rec != '' and elem.tag.endswith('}p') and len(bible_items) > 0 and has_verse_pageheader_pattern():
			# This is a continuation of a verse or footnote in a separate paragraph element.

			item = bible_items[len(bible_items) - 2]
			item.text = concat_lines(item.text, get_text_rec(elem))
		#elif has_verse_to_continue_before_page_break() and elem.tag.endswith('}p') and elem_text_rec != '' and not is_parent_of_last_bible_item(elem):
		#	verse = get_verse_before_page_break()
		#	verse.text = concat_lines(verse_text, elem_text_rec)
		elif elem_text != None and elem.tag.endswith('}p') and is_parallel_passage_ref(elem_text):
			bible_items.append(ParallelPassageReference(get_parallel_passage_ref(elem_text), elem))

	bible_items = model_post_processor.process(bible_items)

	usfm_writer.write(bible_items)

	#todo:Ung daang la 'piili 'wulibu a mani nuoring. 


if __name__ == "__main__":
	main()
