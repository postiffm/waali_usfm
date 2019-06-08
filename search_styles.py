import xml.etree.ElementTree as ET

from sugar import *


for event, elem in ET.iterparse('content_indented.xml', events = ['end']):
	if elem.tag.endswith('}style'):
		name_attrib = one_where(elem.attrib, lambda attrib_name: attrib_name.endswith('name'))
		name = elem.attrib[name_attrib]
		properties_el = one_where(elem.getchildren(), lambda child: child.tag.endswith('paragraph-properties'))
		if properties_el == None:
			continue
		margin_left_attrib = one_where(properties_el.attrib, lambda attrib_name: attrib_name.endswith('margin-left'))
		if margin_left_attrib == None:
			continue
		margin_left = properties_el.attrib[margin_left_attrib]
		margin_left_num = float(margin_left[0:len(margin_left) - 2])
		print(margin_left_num)