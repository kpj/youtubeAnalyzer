def apply(comments, args):
	return [com for com in comments if com["upvotes"] - com["downvotes"] < 0]
