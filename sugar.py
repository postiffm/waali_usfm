
def pipe(input, *funcs):
	for f in funcs:
		input = f(input)
	return input


def last(mylist):
	return mylist[len(mylist) - 1]
