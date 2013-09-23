def apply(comments, args):
	return sum(len(com["text"]) for com in comments) / len(comments)
