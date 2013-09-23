def apply(comments, args):
	out = []
	for com in comments:
		if com["upvotes"] - com["downvotes"] < 0:
			out.append(com)
	return out
