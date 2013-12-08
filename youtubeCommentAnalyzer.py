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

    def get_all_vids(self, index):
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
        if self.videos != None:
            return self.videos

        raw_videos = self.get_all_vids(1)

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
    def __init__(self, url):
        self.id = re.findall(r'www.youtube.com/watch\?v=(.*)', url)[0]

        self.comments = None

    def get_comments(self, page_num=1):
        if self.comments == None:
            self.comments = []

            for p in range(1, page_num + 1):
                com_data_url = "http://www.youtube.com/all_comments?v=%s&page=%i" % (self.id, p)
                soup = BeautifulSoup(urllib.urlopen(com_data_url))
                for dat in soup.findAll("div", {"class": "content clearfix"}):
                    cur_com = {}

                    # check if comment was deleted
                    if dat.find("p").find("em") == None:
                        # find text
                        text = ""
                        container = dat.find("div", {"class": "comment-text"})
                        if container.find("p") != None:
                            text = container.find("p").text
                        else:
                            text = container.text

                        # find author
                        meta = dat.find("p", {"class": "metadata"})
                        author = meta.find("span", {"class": "author"}).find("a").text

                        # find additional info
                        action = dat.find("div", {"class": "comment-actions"})
                        upvotes_data = action.find("span", {"class": "comments-rating-positive"})
                        upvotes = 0
                        downvotes = 0
                        if upvotes_data != None:
                            m = re.match(r'\D*?(\d+)\D*?(\d+)\D*?', upvotes_data.get("title"))
                            upvotes = int(m.groups()[0])
                            downvotes = int(m.groups()[1])

                        # throw it all together
                        cur_com["text"] = text
                        cur_com["author"] = author
                        cur_com["upvotes"] = upvotes
                        cur_com["downvotes"] = downvotes

                        self.comments.append(cur_com)

        return self.comments

    def applyFilter(self, filter, *args):
        if self.comments == None:
            self.get_comments()
        return filter.apply(self.comments, *args)


#vid = YoutubeVideo(sys.argv[1])

#pprint(vid.applyFilter(filters.all_caps))
#print vid.applyFilter(filters.average_comment_length)
#pprint(vid.applyFilter(filters.scan_for_regexp, "[Mm]inecraft"))
#pprint(vid.applyFilter(filters.highest_vote))
#pprint(vid.applyFilter(filters.show_downvoted))
#pprint(vid.applyFilter(filters.scan_wordlist, os.path.join("filters", "data", "smileys.txt"), True))

chan = YoutubeChannel(sys.argv[1])
pprint(chan.apply_filter(filters.gameone))
