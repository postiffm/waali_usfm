import os
import waali_parser as parser
from model import get_printable_items

def write(bible_items, path):
	printable_items = get_printable_items(bible_items)
	f = open(path, 'w')
	for item in printable_items:
		f.write(str(item) + '\n')
	f.close()

def read_all_text(filepath):
	f = open(filepath, 'r')
	text = f.read()
	f.close()
	return text

def main():
	test_inputs = [f for f in os.listdir('tests') if f.endswith('.xml')]

	failed = False

	for f in test_inputs:
		test_name = os.path.splitext(f)[0]

		path_to_expected = './tests/expected/' + test_name + '.usfm'
		path_to_actual = './tests/actual/' + test_name + '.usfm'

		bible_items = parser.parse('./tests/' + f)
		write(bible_items, path_to_actual)

		if not os.path.isfile(path_to_expected):
			print('Failed ' + test_name + ': Could not find expected usfm. Looked for ' + path_to_expected)
		elif not os.path.isfile(path_to_actual):
			print('Failed ' + test_name + ': Could not find actual usfm. Looked for ' + path_to_actual)
		else:
			expected = read_all_text(path_to_expected)
			actual = read_all_text(path_to_actual)
			if expected.strip() != actual.strip():
				print('Failed ' + test_name + ': expected != actual. Expected: ' + expected + ' actual ' + actual)

	print('Succeeded' if not failed else 'Failed')

if __name__ == "__main__":
	main()
