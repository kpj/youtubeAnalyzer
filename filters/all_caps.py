def is_upper_case(string):
	for c in string:
		if c.islower():
			return False
	return True

def apply(comments, args):
	return [com for com in comments if is_upper_case(com["text"])]
