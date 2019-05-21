import waali_parser as parser
import usfm_writer
import model_post_processor

def main():

	bible_items, errors = model_post_processor.process(parser.parse('content_indented_no_noise.xml'))

	usfm_writer.write(bible_items, '../usfm_out_rev2')

	for e in errors:
		print(str(e))


if __name__ == "__main__":
	main()
