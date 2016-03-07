#!/usr/bin/env python
import sys
import rfc822
import time
import json
from sqlite3 import connect
from urllib import urlopen, urlencode
from tweetconnect import *
from auth_and_Secret import TweetOuth

c = None
tweet_id = None

def load_tweets(**kwargs):
    args = dict(trim_user=1)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/statuses/show.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url)
    tweet=json.loads(user_timeline)    
    if type(tweet) == dict and tweet.has_key(u'errors'):
        raise Exception(tweet[u'errors'])         
    print "text: ",tweet[u'text']
    print "hashtags: "
    for twit in range(len(tweet['entities']['hashtags'])):
        print tweet['entities']['hashtags'][twit][u'text']
    print "references: "
    for twit in range(len(tweet['entities']['user_mentions'])):
        print tweet['entities']['user_mentions'][twit][u'screen_name']
    print "Favorite Count: ", tweet['favorite_count']
    print "Retweet Count: ", tweet['retweet_count']

def print_help(args):
    print >>sys.stderr, '''
Usage:

    %s  <tweet_id>

show data of tweet
''' % args[0]

def main(*args):
    global c, tweet_id
    if len(args) != 2:
        print_help(args)
    else:
        tweet_id=args[1]
        load_tweets(id=tweet_id)
        
        
if __name__ == '__main__':
    main(*sys.argv)
