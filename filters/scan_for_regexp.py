import re

def apply(comments, regexp):
	print regexp
	return [com for com in comments if re.search(regexp, com["text"]) != None]
