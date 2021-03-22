from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import TwitterCredentials

class stdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

        
if  __name__ == "__main__":

    listener = stdOutListener()
    auth = OAuthHandler(TwitterCredentials.CONSUMER_KEY, TwitterCredentials.CONSUMER_SECRET)
    auth.set_access_token(TwitterCredentials.ACCESS_TOKEN, TwitterCredentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=['barcelona', 'real madrid'])