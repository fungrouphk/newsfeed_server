from HTMLParser import HTMLParser
from clustering import Vector, Cluster
from collections import Counter
import Queue
import clustering
import feedparser
import jieba
import jieba.posseg as pseg
import time
from db import News
import json

meaninglessWords = (u"　", u"，", u"。", u":", u"會", u"「", u"」", u"有", u"...", u"在", u"的", u"被", u"及", u"他", u"與", u"但", u"是", u"時", u"為", u"和", u"就", u"上", u"到", u"因為", u"向", u"於", u"他們", u"其中", u"沒有", u"指", u"將", u"才")

# only consider certain type of word
def preprocess(segList):
    # w.flag in ["a", "an", "i", "j", "l", "m", "n", "nr", "ns", "nt", "nz", "tg", "t", "vg", "v", "vd", "vn", "x"] and 
    return [w for w in segList if w not in meaninglessWords]

def getBagOfWords(segList):
    return Counter(segList)
                
class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

# remove html tag
def stripTag(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()


def printList(l):
    print repr(l).decode("unicode_escape")


def run():
    start_time = time.clock()
    jieba.set_dictionary('jieba/dict.txt.big')
    jieba.initialize()
    print ("jieba " + str(time.clock() - start_time))
    
    start_time = time.clock()

    news_rss_url = "http://hk.news.yahoo.com/rss/hong-kong"
    # news_rss_url = "http://hk.news.yahoo.com/rss/china"
    info = feedparser.parse(news_rss_url)

    
    start_time = time.clock()

    for entry in info.entries:
        # word count of each word of summary
        word_list = getBagOfWords(preprocess(jieba.cut(stripTag(entry.summary))))
        # word count of each word of title
        bag_of_word_of_title = getBagOfWords(preprocess(jieba.cut(stripTag(entry.title))))
        
        # Combine word count of both summary and title and title weights more
        bag_of_word = Counter()
        for i in range(3):
            bag_of_word.update(bag_of_word_of_title)
        bag_of_word.update(word_list)
        entry["bag_of_words"] = bag_of_word

    print ("preprocess " + str(time.clock() - start_time))
        

#     result = Counter()
#     for entry in info.entries:
#         result.update(entry["bag_of_words"])
#     printList(result) 
        
    # Clustering them
    start_time = time.clock()
    clusters = clustering.clustering([Cluster([Vector(entry)]) for entry in info.entries])
    print ("clustering " + str(time.clock() - start_time))

    # Print the result        
    newsList = []
    for (index, cluster) in enumerate(clusters):
        for vector in cluster.listOfVectors:
            news = News(index, (vector == cluster.centroidVector), vector.data["title"], vector.data["published"], vector.data["link"])
            newsList.append(news.__dict__)
    return json.dumps(newsList)


if __name__ == "__main__":
    print run()
    
