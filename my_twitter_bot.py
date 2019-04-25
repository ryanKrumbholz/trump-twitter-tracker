import tweepy
import datetime
import time

CONSUMER_KEY = 'your key' #twitter developer consumver ID
CONSUMER_SECRET = 'your key' #twitter developer consumer secret
ACCESS_KEY = 'your key' #twitter developer access key
ACCESS_SECRET = 'your key' #twitter developer secret

auth =  tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) #creating the authentication
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

def write_last_id(id): #writes mention tweet id to txt file to prevent duplicate responses
    f = open('uniqueIDs.txt','w')
    f.write(str(id))
    f.close()
    
def read_last_id(): #reads from txt file to prevent duplicate responses
    f = open('uniqueIDs.txt','r')
    lastid = int(f.read().strip())
    f.close()
    return lastid

def count_tweets():
    tweets = api.user_timeline('@realDonaldTrump') #tweets from Donald Trump's twitter
    last_seen_id = read_last_id()
    mentions = api.mentions_timeline(last_seen_id) #only mentions that haven't been seen yet
    count = 0 #number of tweets per day
    today = time.localtime()[2] #today's day of the month (numerically)
    
    def tweet_oncommand():
        current_time = str(time.localtime()[3]) + 'hrs ' + str(time.localtime()[4]) + 'mins ' + str(time.localtime()[5]) + 'secs'
        for mention in reversed(mentions): #iterating through all unseen mentions
            user = mention.user.screen_name #twitter username
            last_seen_id = mention.id #updating last_seen_id
            if '#count' in mention.text:
                print("Count command made")
                api.update_status("@" + user + " Trump has tweeted " + str(count) + " times so far today as of " + current_time + "! (including retweets)")
                write_last_id(str(last_seen_id))
                print("Status updated")

    def tweet_count_midnight():
        yesterday = datetime.date.today() - datetime.timedelta(1)
        midnight = time.localtime()[3] == 0 and time.localtime()[4] == 0 and time.localtime()[5] <= 15 #bool that is true when it is midnight
        if midnight:
            print("Tweeting midnight status")
            api.update_status("Yesterday (" + yesterday.strftime('%m/%d/%Y') + ") Trump tweeted " + str(count) + " times! (including retweets)")
            print("Status tweeted")
    
    for tweet in tweets: #iterates through DT tweets
        if tweet.created_at.timetuple()[2] == today: #if the tweet was made today then update the count
            count +=1
        if tweet.created_at.timetuple()[2] < today: #if the tweet wasn't made today the loop breaks. this prevents prior month's tweets from being counted
            break

    tweet_oncommand()
    tweet_count_midnight()

while True:
    count_tweets()
    time.sleep(15)
