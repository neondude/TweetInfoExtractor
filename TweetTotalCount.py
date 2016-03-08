import sys
import json
from urllib import urlopen, urlencode
from tweetconnect import *
from auth_and_Secret import TweetOuth

c = None
screen_name = None
reTweetCount=0
favoriteCount=0
tweet_max_id=0

        

def fetch():    
    tweet_count=load_tweets()
    going_down=True
    while going_down:        
        print "Requesting tweets older than ",tweet_max_id
        tweet_count = load_tweets(max_id=tweet_max_id)
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    global reTweetCount,favoriteCount,tweet_max_id
    args = dict( count=100,trim_user=1,include_rts=False, screen_name=screen_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url)
    tweets=json.loads(user_timeline)
    if len(tweets)>0:        
        for twit in tweets:
            reTweetCount+=twit['retweet_count']
            favoriteCount+=twit['favorite_count']
            tweet_max_id=twit['id']
    return len(tweets)-1

def print_help(args):
    print >>sys.stderr, '''
Usage:

    %s <username>

returns total number of retweets and favorites for a username
''' % args[0]

def main(*args):
    global screen_name
    
    if len(args) != 2:
        print_help(args)
    else:
        screen_name=args[1]
        fetch()
        print "Retweet Total= ",reTweetCount
        print "Favorite Total= ",favoriteCount
    
    

if __name__ == '__main__':
    main(*sys.argv)
