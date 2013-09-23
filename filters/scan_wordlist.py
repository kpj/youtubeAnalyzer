def apply(comments, args):
	out = []
	wordlist_path = args[0]
	accept = args[1]

	all_words = filter(None, open(wordlist_path, "r").read().split("\n"))

	for com in comments:
		if accept:
			if any(word.lower() in com["text"].lower() for word in all_words):
				out.append(com)
		else:
			if not any(word.lower() in com["text"].lower() for word in all_words):
				out.append(com)

	return out
