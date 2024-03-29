
import book_info

class Printable(object):
	pass
class VersePart(object):
	pass

class Book(Printable):
	def __init__(self, name, elem):
		self.name = name
		self.elem = elem

	def __str__(self):
		book_id = book_info.books[self.name]['id']
		return f"""\\id {book_id}
\\h {self.name}
\\mt1 {self.name}
\\toc1 {self.name}
\\toc2 {self.name}
\\toc3 {book_id}"""

class Heading(Printable):
	def __init__(self, text, elem):
		self.text = text
		self.elem = elem

	def __str__(self):
		return f'\\s {self.text}'

class Chapter(Printable):
	def __init__(self, number, elem):
		self.number = number
		self.elem = elem

	def __str__(self):
		return f'\\c {self.number}'

class Verse(Printable, VersePart):
	def __init__(self, number, text, elem, starts_indented=False):
		self.number = number
		self.text = text
		self.elem = elem
		self.starts_indented = starts_indented

	def __str__(self):
		q = r' \q1' if self.starts_indented else ''
		return f"\\v {self.number}{q} {self.text}"

class FootNote:
	def __init__(self, chapter_num, verse_num, text, elem):
		self.chapter_num = chapter_num
		self.verse_num = verse_num
		self.text = text
		self.elem = elem

class PageHeader:
	def __init__(self, elem):
		self.elem = elem

class ParallelPassageReference(Printable):
	def __init__(self, text, elem):
		self.elem = elem
		self.text = text

	def __str__(self):
		return f"\\r {self.text}"

class Paragraph(Printable, VersePart):
	def __init__(self, text, elem):
		self.elem = elem
		self.text = text

	def __str__(self):
		return rf"\p {self.text}"

# corresponds to either poetic line or indented quote, both of which are represented by \q1 in usfm.
class Indentation(Printable, VersePart):
	def __init__(self, text, elem):
		self.elem = elem
		self.text = text
	def __str__(self):
		return rf"\q1 {self.text}"

# https://ubsicap.github.io/usfm/titles_headings/index.html#rq-rq
# todo: doesn't look like the below class is used. Delete if not used.
class ParallelPassageRef(Printable):
	def __init__(self, text, elem):
		self.elem = elem
		self.text = text
	def __str__(self):
		return rf"\r {self.text}"
