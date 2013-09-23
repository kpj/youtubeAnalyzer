def apply(comments, args):
	max_com = None
	for com in comments:
		if max_com == None:
			max_com = com
			continue
		if com["upvotes"] - com["downvotes"] > max_com["upvotes"] - max_com["downvotes"]:
			max_com = com
	return max_com
