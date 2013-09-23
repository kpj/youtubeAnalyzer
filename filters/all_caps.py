def is_upper_case(string):
	for c in string:
		if c.islower():
			return False
	return True

def apply(comments, args):
	upper = []

	for com in comments:
		if is_upper_case(com["text"]):
			upper.append(com)

	return upper
