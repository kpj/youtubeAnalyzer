def apply(comments, args):
	return max(comments, key = lambda x: x['upvotes'] - x['downvotes'])
