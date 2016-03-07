#!/usr/bin/env python
import sys
import json
from sqlite3 import connect
from urllib import urlopen, urlencode
from tweetconnect import *
from auth_and_Secret import TweetOuth

c = None
screen_name = None


def display():
    tagList = []
    space = ''
    cursor = c.execute('SELECT tags from hashtag')
    for row in cursor:
        text = ''
        for field in row:
            field.encode('ascii','ignore')
            text+=field
        tagList.append(text)
    for tag in list(set(tagList)):
        print tag
        

def fetch():    
    going_up = True
    while going_up:
        cu = c.cursor()
        cu.execute('SELECT MAX(tweet_id) max_id FROM hashtag')
        results = cu.fetchone()
        tweet_count = None        
        if not results[0]:
            print >>sys.stderr, 'No existing tweets found: requesting default timeline.'
            tweet_count = load_tweets()
        else:
            print >>sys.stderr, 'Requesting tweets newer than %lu' % results[0]
            tweet_count = load_tweets(since_id=results[0])
        if tweet_count==0:
            going_up = False    
    going_down = True
    while going_down:
        cu = c.cursor()
        cu.execute('SELECT MIN(tweet_id) min_id FROM hashtag')
        results = cu.fetchone()
        print >>sys.stderr, 'Requesting tweets older than %lu' % results[0]
        tweet_count = load_tweets(max_id=(results[0]-1))
        # The -1 is lame, but max_id is "<=" not just "<"
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    args = dict(count=20, trim_user=1, screen_name=screen_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url)
    tweets=json.loads(user_timeline)    
    if type(tweets) == dict and tweets.has_key(u'errors'):
        raise Exception(tweets[u'errors'])         
    for twit in tweets:
        if len(twit['entities']['hashtags'])>0:
            for n in range(len(twit['entities']['hashtags'])):
                c.execute('INSERT INTO hashtag (tweet_id,tags) VALUES (?,?)',(twit['id'],twit['entities']['hashtags'][n][u'text'])) 
        else:
            c.execute('INSERT INTO hashtag (tweet_id,tags) VALUES (?,?)',(twit['id'],""))
    c.commit()
    return len(tweets)

def print_help(args):
    print >>sys.stderr, '''
Usage:

    %s <operation> <username>

Operations:

    * init: Create an initial <username>.db file.
    * fetch: Fill in missing hashtags for <username>.db
    * display: Display all hashtags used by <username>
''' % args[0]

def main(*args):
    global c, screen_name
    
    if len(args) != 3:
        print_help(args)
    
    elif args[1] == 'init':
        screen_name = args[2]
        try:
            c = connect('%s.db' % screen_name)
            c.execute('CREATE TABLE hashtag (tweet_id INTEGER,tags TEXT)')
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem creating your database: %s" % str(e)
            sys.exit(-1)
    
    elif args[1] == 'fetch':
        screen_name = args[2]
        try:
            c = connect('%s.db' % screen_name)
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem opening your database: %s" % str(e)
            sys.exit(-2)
        try:
            fetch()
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem retrieving %s's timeline: %s" % (screen_name, str(e))
            print >>sys.stderr, "Error: This may be a temporary failure, wait a bit and try again."
            sys.exit(-3)
            
    elif args[1] == 'display':
        screen_name = args[2]
        try:
            c = connect('%s.db'%screen_name)
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem opening your database: %s" % str(e)
            sys.exit(-2)
        try:
            display()
        except Exception, e:
            print str(e)
        
    
    else:
        print_help(args)
    

if __name__ == '__main__':
    main(*sys.argv)
