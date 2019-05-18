

def get_text_rec(elem):
	parts = []
	if elem.text:
		parts.append(elem.text)
	for item in elem:
		if item.text:
			parts.append(item.text)
		if item.tail:
			parts.append(item.tail)
	return ''.join(parts)
