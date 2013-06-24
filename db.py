from pymongo import MongoClient


class News:
    def __init__(self, clusterId, isCentroid, title, pubDate, url):
        self.title = title
        self.clusterId = clusterId
        self.isCentroid = isCentroid
        self.pubDate = pubDate
        self.url = url
    def save(self):
        client = MongoClient()
        db = client.test_database
        db.news.insert(self.__dict__)
        
    @staticmethod
    def getLatest():
        client = MongoClient()
        db = client.test_database
        return db.news.find().sort("_id" , -1).limit(1)[0];
    
    @staticmethod
    def printAll():
        client = MongoClient()
        db = client.test_database        
        all_news = db.news.find()
        for news in all_news:
            print news
        
        
if __name__ == "__main__":
    news = News("title", "smmary", "pubData", "url")
    news.save()
    print News.getLatest()
