import unittest
import bible_diff

class MockFilesProvider:
	def __init__(self, file_providers):
		self.file_providers = file_providers

	def list_files(self):
		return self.file_providers

class MockFileProvider:
	def __init__(self, text):
		self.text = text

	def load_lines(self):
		return self.text.splitlines()

class MyTests(unittest.TestCase):

    def test_load_bible(self):
    	book1 = MockFileProvider(r"""
\id GEN
\h book one
\mt1 book one
\toc3 GEN
\c 1
\v 1 verse one
\s section one
\v 2 verse two
\c 2
\v 1 verse one of chapter two
    		""")
    	book2 = MockFileProvider(r"""
\id ABC
\h book two
\mt1 book two
\toc3 ABC
\c 1
\v 1 blah blah
\q1 a quote
\r parallel passage ref
\c 2
\v 1 verse one of chapter two
\p a paragraph
    		""")

    	files = MockFilesProvider([book1, book2])

    	bibles = bible_diff.load_bible(files)

    	self.assertTrue(bibles['book one'])
    	self.assertTrue(bibles['book one'].chapters[1])
    	self.assertTrue(bibles['book one'].chapters[1].verses[1])
    	self.assertTrue(bibles['book one'].chapters[1].verses[1].text == "verse one")
    	self.assertTrue(bibles['book one'].chapters[1].verses[2])
    	self.assertTrue(bibles['book one'].chapters[1].verses[2].text == "verse two")
    	self.assertTrue(bibles['book one'].chapters[2])
    	self.assertTrue(bibles['book two'])
    	self.assertTrue(bibles['book two'].chapters[1].verses[1])
    	self.assertEqual(bibles['book two'].chapters[1].verses[1].text, "blah blah a quote")
    	self.assertTrue(bibles['book two'].chapters[2])
    	self.assertTrue(bibles['book two'].chapters[2].verses[1])
    	self.assertEqual(bibles['book two'].chapters[2].verses[1].text, "verse one of chapter two a paragraph")

if __name__ == '__main__':
    unittest.main()