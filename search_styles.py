import xml.etree.ElementTree as ET

from sugar import *

def find_indented_paragraph_styles():
	indented_paragraph_styles = []
	for event, elem in ET.iterparse('content_indented.xml', events = ['end']):
		if elem.tag.endswith('}style'):
			name_attrib = one_where(elem.attrib, lambda attrib_name: attrib_name.endswith('name'))
			name = elem.attrib[name_attrib]
			paragraph_properties_el = one_where(elem.getchildren(), lambda child: child.tag.endswith('paragraph-properties'))
			if paragraph_properties_el == None:
				continue

			margin_left_attrib = one_where(paragraph_properties_el.attrib, lambda attrib_name: attrib_name.endswith('margin-left'))
			margin_left_num = 0
			if margin_left_attrib != None:
				margin_left = paragraph_properties_el.attrib[margin_left_attrib]
				margin_left_num = float(margin_left[0:len(margin_left) - 2])

			text_indent_attrib = one_where(paragraph_properties_el.attrib, lambda attrib_name: attrib_name.endswith('text-indent'))
			text_indent_num = 0
			if text_indent_attrib != None:
				text_indent = paragraph_properties_el.attrib[text_indent_attrib]
				text_indent_num = float(text_indent[0:len(text_indent) - 2])

			text_align_attrib = one_where(paragraph_properties_el.attrib, lambda attrib_name: attrib_name.endswith('text-align'))
			text_align = ''
			if text_align_attrib != None:
				text_align = paragraph_properties_el.attrib[text_align_attrib]

			font_weight = ''
			text_properties_el = one_where(elem.getchildren(), lambda child: child.tag.endswith('text-properties'))
			if text_properties_el != None:
				font_weight_attrib = one_where(text_properties_el.attrib, lambda attrib_name: attrib_name.endswith('font-weight'))
				if font_weight_attrib:
					font_weight = text_properties_el.attrib[font_weight_attrib]

			if (margin_left_num >= 0.5 or text_indent_num >= 0.5) and text_align != 'center' and font_weight != 'bold':
				indented_paragraph_styles.append(name)

	styles_set = ", ".join(f"'{f}'" for f in indented_paragraph_styles)
	styles_set = "{" + styles_set + "}"
	print(styles_set)


find_indented_paragraph_styles()

