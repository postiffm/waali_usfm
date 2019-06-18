
from model import *
from utils import *
from sugar import *

def process(book_name_set, bible_items, elem):
	pattern_match_cache = {}
	matching_patterns = [p for p in patterns if p.Matches(book_name_set, bible_items, elem, pattern_match_cache)]
	if len(matching_patterns) != 1:
		return False, 'Expected 1 matching pattern but found: ' + str(len(matching_patterns)) + "Elem text: " + get_text_rec(elem) + ". Patterns: " + ", ".join([str(p) for p in matching_patterns])
		#print(get_text_rec(elem))
	else:
		matching_patterns[0].Act(book_name_set, bible_items, elem)

	return True, None

def cached_match(matcher, *matcher_args, **matcher_kwargs):
	cache = matcher_args[3] if len(matcher_args) == 4 else matcher_kwargs['cache']
	if matcher in cache:
		return cache[matcher]
	result = matcher(*matcher_args, **matcher_kwargs)
	cache[matcher] = result
	return result

def cached(matcher):
	def decorator(*args, **kwargs):
		return cached_match(matcher, *args, **kwargs)
	return decorator

class PatternBlank(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_white_space(get_text_rec(elem))

	def Act(book_name_set, bible_items, elem):
		pass


class PatternBook(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		text = get_normalized_text(elem).strip()
		return text in book_name_set or \
			text == "' Maatiu Gbangu" # Mathew has an anomolous space between the ' and first letter.

	def Act(book_name_set, bible_items, elem):
		text = get_normalized_text(elem).strip()
		text = "'Maatiu Gbangu" if text == "' Maatiu Gbangu" else text
		bible_items.append(Book(text, elem))

class PatternChapter(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_int(get_text_rec(elem)) and child_count(elem) == 0

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Chapter(int(get_text_rec(elem)), elem))

class PatternFirstVerseWithoutNumber(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		elem_text_rec = get_text_rec(elem)
		return not PatternBlank.Matches(book_name_set, bible_items, elem, cache) and \
		    not has_heading_style(elem) and \
		    not starts_with_verse_num(elem_text_rec) and \
		    not PatternHeadingInSpan.Matches(book_name_set, bible_items, elem, cache) and \
		    has_chapter_or_chapter_header_pattern(bible_items)

	def Act(book_name_set, bible_items, elem):
		bible_items.append(Verse(1, get_text_rec(elem), elem))

class PatternVerseWithNumber(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		text = get_normalized_text(elem)
		# check is_passage_ref_end_part because a reference part can also start with a number.
		return starts_with_verse_num(get_text_rec(elem)) and \
		    not PatternChapterInSpan.Matches(book_name_set, bible_items, elem, cache) and \
			not PatternChapter.Matches(book_name_set, bible_items, elem, cache) and \
		    not is_passage_ref_end_part(text) and \
			not PatternHeadingAndChapterInSameParagraph.Matches(book_name_set, bible_items, elem, cache)

	def Act(book_name_set, bible_items, elem):
		# todo: handle Psalms style verse 1's where the v 1 has a number and follows a heading.
		elem_text_rec = get_text_rec(elem)
		verse_num = get_verse_num(elem_text_rec)
		verse_text = elem_text_rec[len(str(verse_num)):].strip()
		verse_text = normalize_space(verse_text)
		starts_indented = verse_starts_indented(elem)
		bible_items.append(Verse(verse_num, verse_text, elem, starts_indented))

@cached
def is_verse_text_with_no_verse_number(book_name_set, bible_items, elem, cache):
	return not starts_with_verse_num(get_normalized_text(elem)) and \
		not PatternBlank.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternPageHeader.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternStartOfFootNotes.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternFootNote.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternChapter.Matches(book_name_set, bible_items, elem, cache) and \
		not has_heading_style(elem) and \
		not PatternVerseWithNumber.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternChapterInSpan.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternParallelPassage.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternHeadingInSpan.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternBook.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternPsalmNumber.Matches(book_name_set, bible_items, elem, cache) and \
		not PatternCrossReferenceEndPart.Matches(book_name_set, bible_items, elem, cache)

# todo: check if some indented quotes are interrupted by a page header.
# If so, this pattern will need to be changed to something like "PatternAppendableContinuation"
# to handle both verses and quotes.
# Or perhaps there's another way to appended together the parts cut by a page header,
# like post processing.
class PatternVerseContinuation(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_verse_text_with_no_verse_number(book_name_set, bible_items, elem, cache) and \
			not PatternIndentation.Matches(book_name_set, bible_items, elem, cache) and \
			last_printable_item_is(bible_items, Verse)

	def Act(book_name_set, bible_items, elem):
		last_verse = last_printable_item(bible_items)
		concat_with_last_verse = lambda t : concat_lines(last_verse.text, t)
		last_verse.text = pipe(elem, get_text_rec, normalize_space, concat_with_last_verse)

def add_or_append_heading(bible_items, elem):
	text = get_normalized_text(elem)
	if len(bible_items) > 0 and isinstance(last(bible_items), Heading):
		last(bible_items).text = concat_lines(last(bible_items).text, text)
	else:
		bible_items.append(Heading(text, elem))

class PatternHeading(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return not PatternBlank.Matches(book_name_set, bible_items, elem, cache) and \
			has_heading_style(elem)
	def Act(book_name_set, bible_items, elem):
		add_or_append_heading(bible_items, elem)

class PatternHeadingInSpan(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return any(elem.getchildren(), lambda child: has_heading_style(child) and has_equivalent_text(elem, child)) and \
			not is_int(get_normalized_text(elem)) # not a chapter in a span.
	def Act(book_name_set, bible_items, elem):
		add_or_append_heading(bible_items, elem)

class PatternHeadingAndChapterInSameParagraph(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		children = elem.getchildren()
		return len(children) > 1 and \
			children[0].text != None and \
			is_int(children[0].text.strip()) and \
			any(children[1:], lambda child: has_heading_style(child) and child.text != None and not child.text.isspace())
	def Act(book_name_set, bible_items, elem):
		children = elem.getchildren()
		chapter = int(children[0].text.strip())
		heading = one_where(children[1:], lambda child: has_heading_style(child) and not child.text.isspace()).text
		bible_items.append(Chapter(chapter, elem))
		bible_items.append(Heading(heading, elem))


class PatternChapterInSpan(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		children = elem.getchildren()
		return len(children) == 2 and has_style(children[0], 'T5') and is_int(children[0].text)
	def Act(book_name_set, bible_items, elem):
		children = elem.getchildren()
		bible_items.append(Chapter(int(children[0].text), elem))
		bible_items.append(Verse(1, normalize_space(get_text_rec(children[1])), elem))

class PatternPageHeader(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_page_header(pipe(elem, get_text_rec, normalize_space))
	def Act(book_name_set, bible_items, elem):
		bible_items.append(PageHeader(elem))

class PatternStartOfFootNotes(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return get_text_rec(elem).strip() == '*________'
	def Act(book_name_set, bible_items, elem):
		pass

class PatternFootNote(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return starts_with_footnote_ref(get_text_rec(elem))
	def Act(book_name_set, bible_items, elem):
		footnote_chapter, footnote_verse = get_footnote_ref(get_text_rec(elem))
		footnote_text = get_footnote_text(elem)
		bible_items.append(FootNote(footnote_chapter, footnote_verse, footnote_text, elem))

class PatternParallelPassage(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_passage_ref(get_text_rec(elem)) and has_parallel_passage_ref_style(elem)
	def Act(book_name_set, bible_items, elem):
		bible_items.append(ParallelPassageReference(get_passage_ref(get_text_rec(elem)), elem))

class PatternCrossReferenceEndPart(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_passage_ref_end_part(get_text_rec(elem)) and last_printable_item_is(bible_items, VersePart)
	def Act(book_name_set, bible_items, elem):
		last_printable = last_printable_item(bible_items)
		last_printable.text = concat_lines(last_printable.text, get_normalized_text(elem))

class PatternParagraph(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_verse_text_with_no_verse_number(book_name_set, bible_items, elem, cache) and \
			not last_printable_item_is(bible_items, Verse) and \
			not PatternFirstVerseWithoutNumber.Matches(book_name_set, bible_items, elem, cache) and \
			not has_indented_style(elem) # not quote or reference quote
	def Act(book_name_set, bible_items, elem):
		text = normalize_space(get_text_rec(elem)).strip()
		if last_printable_item_is(bible_items, Paragraph):
			p = last_printable_item(bible_items)
			p.text = concat_lines(p.text, text)
		else:
			bible_items.append(Paragraph(text, elem)) 

class PatternPsalmNumber(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return is_psalm_number(get_normalized_text(elem))
	def Act(book_name_set, bible_items, elem):
		bible_items.append(Chapter(get_psalm_number(get_normalized_text(elem)), elem))

class PatternIndentation(object):
	@cached
	def Matches(book_name_set, bible_items, elem, cache):
		return has_indented_style(elem) and not PatternCrossReferenceEndPart.Matches(book_name_set, bible_items, elem, cache)
	def Act(book_name_set, bible_items, elem):
		bible_items.append(Indentation(get_normalized_text(elem), elem))

# todo: what's this? a parallel reference in a footnote? ('Yiibu G. 25:7; Soribu G. 11:7)

patterns = [PatternBlank, PatternBook, PatternChapter,
	PatternFirstVerseWithoutNumber, PatternVerseWithNumber, PatternHeading, PatternHeadingInSpan,
	PatternHeadingAndChapterInSameParagraph, PatternChapterInSpan, PatternVerseContinuation, PatternPageHeader,
	PatternStartOfFootNotes, PatternFootNote, PatternParallelPassage, PatternCrossReferenceEndPart, PatternParagraph,
	PatternPsalmNumber, PatternIndentation]