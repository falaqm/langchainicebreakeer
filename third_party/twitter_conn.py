import json

def scrape_user_tweets(username,num_tweets=5,mock=True):
    """Scrapes a Twitter users original tweets and returns them
    as a list if dictionary
    """
    if mock:
        tweets = json.load(open("twitter.json","r",encoding="utf-8"))
    tweet_list = []
    for tweet in tweets:
        tweet_dict ={}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet["id"]}"
        tweet_list.append(tweet_dict)
    return tweet_list

if __name__=="__main__":
    tweets = scrape_user_tweets(username="EdenEmarco177")
    print(tweets)