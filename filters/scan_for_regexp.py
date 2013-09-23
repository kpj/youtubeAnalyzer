import re

def apply(comments, args):
	out = []
	pat = args[0]

	for com in comments:
		if re.search(pat, com["text"]) != None:
			out.append(com)

	return out
