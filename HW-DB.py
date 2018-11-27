# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

## [PART 1]
# Finish the function get_tweets that searches for all tweets created by the user "umsi" and 
# all tweets that mention "umsi"
# It takes as input the api object, the cache dictionary, and the cache file name
# It caches the data and will use the cached data if it exists


def get_tweets(api, cacheDict, fname):
	

    # if the data is in the dictionary return it
    searchTerm = "umsi"
    if searchTerm in cacheDict:
        print("Using data from cache")
        fetch = cacheDict[searchTerm]
    # otherwise get the data, add it the dictionary, and write it to a file
    else:
        print("Fetching tweets")
        fetch = api.search(q = searchTerm)
        cacheDict[searchTerm] = fetch

        # get tweets by the umsi user
        
        # get tweets that mention umsi
        
        # add both to the dictionary
        
        # write out the dictionary as JSON
        
    #print(json.dumps(fetch, indent = 4 , sort_keys = True))
    #first = fetch[1]
    #print(json.dumps(first, indent = 2, sort_keys = True))
    #print(first.keys())
    #print('------------------')
    #print(first['retweet_count'])
    return fetch


## [PART 2]
# 
# Finish the function setUpTweetTable that takes a list of tweets, a sqlite connection object, and a cursor and inserts the tweet information in the database
# Fist create a database: tweets.sqlite,
# Then load all of the tweets into a table called Tweets, with the following columns in each row:
## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted
def setUpTweetTable(tweetList, conn, cur):
	tweet_ids = []
	tweet_authors = []
	tweet_times = []
	tweet_text = []
	retweet_counts = []
	counter = 0
	for tweet in tweetList:
		counter += 1
		tweet_ids.append(tweet['id'])
		user = tweet['user']
		screen_name = user['screen_name']
		tweet_authors.append(screen_name)
		tweet_times.append(tweet['created_at'])
		tweet_text.append(tweet['text'])
		retweet_counts.append(tweet['retweet_count'])
	cur.execute('DROP TABLE IF EXISTS Tweets')
	cur.execute('CREATE TABLE Tweets(id INTEGER, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets INTEGER)')
	for x in range(counter):
		cur.execute('INSERT INTO Tweets(id, author, time_posted, tweet_text, retweets) VALUES (?,?,?,?,?)' , (tweet_ids[x], tweet_authors[x], tweet_times[x], tweet_text[x], retweet_counts[x]))
	print(cur)
	pass

## [PART 3]
# Finish the function getTimeAndText that returns a list of strings that contain the 
# time_posted and the text of the tweets.  It takes a database cursor as input.
# Select the time_posted and tweet_text from the Tweets table in tweets.sqlite and return a list 
# of strings that contain the date/time and text of each tweet in the form: date/time - text as shown below
# Mon Oct 09 16:02:03 +0000 2017 - #MondayMotivation https://t.co/vLbZpH390b
def getTimeAndText(cur):
	time_list = []
	text_list = []
	time_and_text_list = []
	cur.execute('SELECT time_posted FROM Tweets')
	for times in cur:
		print(times)
		#time_list.append(times)
	cur.execute('SELECT tweet_text FROM Tweets')
	for text in cur:
		print(text)
		#text_list.append(text)
	count = len(time_list)
	for x in range(count):
		time_and_text_list.append(str(time_list[x] + '-' + text_list[x]))
	print(text_list)
	pass
	
## [Part 4]
# Finish the function getAuthorAndNumRetweets that returns a list of strings for the tweets that have been retweeted MORE than 2 times
# It takes a database cursor as input.
# Select the author (screen name) and number of retweets for of all of the tweets that have been retweeted MORE than 2 times
# Return a list of strings that are in the form: author - # retweets as shown below
# umsi - 5
def getAuthorAndNumRetweets(cur):
	
	pass
		
## Unittests to test the functions
class TestHW9(unittest.TestCase):
	def setUp(self):
		consumer_key = twitter_info.consumer_key
		consumer_secret = twitter_info.consumer_secret
		access_token = twitter_info.access_token
		access_token_secret = twitter_info.access_token_secret
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		
		# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

		# read the cache from the file if it exists
		fname = "twitter_cache.json"
		try:
			cache_file = open(fname,'r')	
			cache_contents = cache_file.read()
			cache_file.close()
			cacheDict = json.loads(cache_contents)
		except:
			cacheDict = {}
    		
		self.conn = sqlite3.connect('tweets.sqlite')
		self.cur = self.conn.cursor()
		self.tweetList = get_tweets(api, cacheDict, fname)
		
	def test_setUpTweetTable(self):
		setUpTweetTable(self.tweetList, self.conn, self.cur)
		self.cur.execute('SELECT * FROM Tweets')
		self.assertEqual(35, len(self.cur.fetchall()))
		
	def test_getTimeAndText(self):
		strList = getTimeAndText(self.cur)
		self.assertEqual(len(strList), 35)
		self.assertEqual(strList[0], 'Tue Nov 13 22:02:48 +0000 2018 - Meet MSI student Huyen Phan and the team that created Peerstachio, the social network and learning community that a… https://t.co/Wyivz99Y73')
		
	def test_getAuthorAndNumRetweets(self):
	    strList = getAuthorAndNumRetweets(self.cur)
	    self.assertEqual(len(strList), 6)
	    self.assertEqual(strList[0], 'umsi - 5')
		

if __name__ == "__main__":
    unittest.main(verbosity=2)
