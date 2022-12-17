import snscrape.modules.twitter as sntwitter
#import twint

class TwitterSceaper():

    def __init__(self, handle):
        self.handle = handle


    def get_tweets(self):


        # Created a list to append all tweet attributes(data)
        attributes_container = []

        # Using TwitterSearchScraper to scrape data and append tweets to list
        prompt = 'from:'+self.handle
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(prompt).get_items()):
            # tweet limit
            if i>200:
                break
            attributes_container.append(tweet.content)
            
        return attributes_container

    # This library didn't work!
    #def twint_get_tweets(self):
    #    c = twint.Config()
    #    c.Limit = 1
    #    c.Username = self.handle
    #    c.Pandas = True
#
    #    twint.run.Search(c)
#
    #    Tweets_df = twint.storage.panda.Tweets_df
#
    #    return Tweets_df


# test cases
#ts = TwitterSceaper("elonmusk")
#print(ts.get_tweets())