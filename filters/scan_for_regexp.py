import re

def apply(comments, args):
	return [com for com in comments if re.search(args[00], com["text"]) != None]
