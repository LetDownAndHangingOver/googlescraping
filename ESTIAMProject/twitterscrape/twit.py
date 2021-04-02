from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pymongo

import TwitterCredentials
import time

class stdOutListener(StreamListener):

    collection_name = "google articles"

    def __init__(self, time_limit = 60):
        self.start_time = time.time()
        self.limit = time_limit
        super(stdOutListener, self).__init__()

    def on_data(self, data):
        if(time.time() - self.start_time) < self.limit:
            try:
                dicto = {}
                self.client = pymongo.MongoClient("mongodb+srv://moe:testtest@cluster0.pmexa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                self.db = self.client["google"]
                all_data = json.loads(data)
                tweet = all_data["text"]
                tweet.encode('utf-16', 'ignore')
                date  = all_data["created_at"]
                authorName  = all_data["user"]["name"]
                authorUserName  = all_data["user"]["screen_name"]
                text = f'{{Author Name : {authorName}, Author UserName : {authorUserName}, Tweet : {tweet}, Date : {date}}}'
                dicto["Nom auteur"] = authorName
                dicto["@"] = authorUserName
                dicto["texte"] = tweet
                dicto["date"] = date
                self.db[self.collection_name].insert_one(dicto)
                output = open("tweet.txt", "a", encoding="utf-8")
                output.write(text)
                output.close()
                print(data)
                return True
            except Exception as e:
                print(e)
        else:
            self.client.close()
            return False     

    
    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    listener = stdOutListener()
    auth = OAuthHandler(TwitterCredentials.CONSUMER_KEY, TwitterCredentials.CONSUMER_SECRET)
    auth.set_access_token(TwitterCredentials.ACCESS_TOKEN, TwitterCredentials.ACCESS_TOKEN_SECRET)


    stream = Stream(auth, listener)

    stream.filter(track=['racisme'], languages=['fr'])