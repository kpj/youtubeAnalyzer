def apply(comments):
	return [com for com in comments if com["upvotes"] - com["downvotes"] < 0]
