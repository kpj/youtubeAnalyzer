def apply(comments):
	return sum(len(com["text"]) for com in comments) / len(comments)
