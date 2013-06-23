from pymongo import MongoClient


class News:
    def __init__(self, title, summary, pubDate, url):
        self.title = title
        self.summary = summary
        self.pubDate = pubDate
        self.url = url
    def save(self):
        client = MongoClient()
        db = client.test_database
        db.news.insert(self.__dict__)
        saved_news = db.news.find_one()       
        
    @staticmethod
    def getLatest():
        client = MongoClient()
        db = client.test_database
        return db.news.find().sort("_id" , -1).limit(1)[0];

        
        
if __name__ == "__main__":
    news = News("title", "smmary", "pubData", "url")
    news.save()
    print News.getLatest()
