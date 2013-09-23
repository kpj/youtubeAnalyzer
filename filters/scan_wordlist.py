def ifnot(b1, b2):
	if b2:
		return b1
	else:
		return not b1

def apply(comments, wordlist_path, accept):
	out = []
	all_words = filter(None, open(wordlist_path, "r").read().split("\n"))

	return [com for com in comments if ifnot(any(word.lower() in com["text"].lower() for word in all_words), accept)]
