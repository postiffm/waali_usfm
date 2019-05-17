
def pipe(input, *funcs):
	for f in funcs:
		input = f(input)
	return input
