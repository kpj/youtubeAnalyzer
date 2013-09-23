def apply(comments):
	return max(comments, key = lambda x: x['upvotes'] - x['downvotes'])
