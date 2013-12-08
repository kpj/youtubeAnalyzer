import sys
import re
import urllib
import os, os.path
import json
from bs4 import BeautifulSoup
from pprint import pprint

import filters


class YoutubeChannel(object):
    def __init__(self, name):
        self.id = name

        self.chunk_size = 50

        self.videos = None

    def get_all_vids(self, index=1):
        com_data_url = "http://gdata.youtube.com/feeds/api/users/%s/uploads?max-results=%i&start-index=%i&alt=json" % (self.id, self.chunk_size, index)
        cont = urllib.urlopen(com_data_url).read()
        data = json.loads(cont)
       
        vids = data["feed"]["entry"]

        more_vids = list()
        if len(vids) == self.chunk_size:
            # grab 'em all
            more_vids = self.get_all_vids(index + self.chunk_size)

        return vids + more_vids

    def parse_videos(self):
        raw_videos = self.get_all_vids()

        res = []
        for v in raw_videos:
            cur = dict()

            cur["title"] = v["title"]["$t"]
            cur["rating"] = v["gd$rating"]["average"]
            cur["views"] = v["yt$statistics"]["viewCount"]
            cur["published"] = v["published"]["$t"]

            res.append(cur)
        return res

    def apply_filter(self, filter, *args):
        if self.videos == None:
            self.videos = self.parse_videos()
        return filter.apply(self.videos, *args)

class YoutubeVideo(object):
    def __init__(self, id):
        self.id = id

        self.comments = None

        self.chunk_size = 50

    def get_all_coms(self, index=1):
        com_data_url = "https://gdata.youtube.com/feeds/api/videos/%s/comments?orderby=published&alt=json&max-results=%i&start-index=%i" % (self.id, self.chunk_size, index)
        cont = urllib.urlopen(com_data_url).read()
        data = json.loads(cont)

        coms = data["feed"]["entry"]

        more_coms = list()
        if len(coms) == self.chunk_size:
            # grab 'em all
            more_coms = self.get_all_coms(index + self.chunk_size)

        return coms + more_coms

    def parse_comments(self):
        raw_comments = self.get_all_coms()

        res = []
        for c in raw_comments:
            cur = dict()

            cur["text"] = c["content"]["$t"]
            cur["author"] = c["author"][0]["name"]["$t"]

            res.append(cur)
        return res

    def applyFilter(self, filter, *args):
        if self.comments == None:
            self.comments = self.parse_comments()
        return filter.apply(self.comments, *args)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <video id/channel name>" % sys.argv[0]
        sys.exit(1)

    query = re.findall(r'www.youtube.com/watch\?v=(.*)', sys.argv[1])
    if len(query) == 1:
        vid = YoutubeVideo(query[0])
        pprint(vid.applyFilter(filters.all_caps))
        print vid.applyFilter(filters.average_comment_length)
        pprint(vid.applyFilter(filters.scan_for_regexp, "[Mm]inecraft"))
        #pprint(vid.applyFilter(filters.highest_vote))
        #pprint(vid.applyFilter(filters.show_downvoted))
        pprint(vid.applyFilter(filters.scan_wordlist, os.path.join("filters", "data", "smileys.txt"), True))
    elif len(query) == 0:
        chan = YoutubeChannel(sys.argv[1])
        pprint(chan.apply_filter(filters.gameone))
    else:
        print "Weird input!"
