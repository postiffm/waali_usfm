import waali_parser as parser
import usfm_writer

def main():
	xml_in = 'content_indented_no_noise_manual_corrections.xml'
	usfm_out = '../usfm_out_rev2'

	print ("Loading input: " + xml_in)
	bible_items, errors = parser.extract_model('content_indented_no_noise_manual_corrections.xml')

	print ("Writing output: " + usfm_out)
	usfm_writer.write(bible_items, '../usfm_out_rev2')

	for e in errors:
		print(str(e))


if __name__ == "__main__":
	main()
