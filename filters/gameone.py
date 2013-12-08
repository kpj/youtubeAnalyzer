import collections

def get_participants(vid):
    both = vid["title"].split("mit")
    if len(both) != 2:
        return None
    names = both[1]
    return [n.strip() for n in names.split("und")]

def apply(videos):
    res = collections.defaultdict(dict)

    # get overall information
    for v in videos:
        ps = get_participants(v)
        if ps != None:
            for p in ps:
                try:
                    res[p]["views"] += int(v["views"])
                except KeyError:
                    res[p]["views"] = int(v["views"])

                try:
                    res[p]["vidnum"] += 1
                except KeyError:
                    res[p]["vidnum"] = 1

                try:
                    res[p]["rating"].append(float(v["rating"]))
                except KeyError:
                    res[p]["rating"] = [float(v["rating"])]

    # calc averages
    ## rating
    bak = {}
    for k, v in res.iteritems():
        all_r = v["rating"]
        if len(all_r) == 0:
            bak[k] = -1
        else:
            bak[k] = sum(all_r) / len(all_r)
    for k, v in bak.iteritems():
        res[k]["rating"] = round(v, 3)
    ## views
    new = {}
    for k, v in res.iteritems():
        new[k] = v["views"] / v["vidnum"]
    for k, v in new.iteritems():
        res[k]["avgviews"] = v

    return dict(res)
