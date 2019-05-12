import tweepy
import datetime
import time

CONSUMER_KEY = 'your key' #twitter developer consumver ID
CONSUMER_SECRET = 'your key' #twitter developer consumer secret
ACCESS_KEY = 'your key' #twitter developer access key
ACCESS_SECRET = 'your key' #twitter developer secret

auth =  tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) #creating the authentication
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def exit():
    print("Exiting program")
    SystemExit()

def write_last_id(id): #writes mention tweet id to txt file to prevent duplicate responses
    f = open('uniqueIDs.txt','w')
    f.write(str(id))
    f.close()

def read_last_id(): #reads from txt file to prevent duplicate responses
    f = open('uniqueIDs.txt','r')
    last_id = int(f.read().strip())
    f.close()
    return last_id

def count_tweets(day_of_month):
    tweets = api.user_timeline('@realDonaldTrump', count = 25, include_rts=False) #tweets from Donald Trump's twitter
    count = 0 #number of tweets per day
    for tweet in tweets: #iterates through DT tweets
        if tweet.created_at.timetuple()[2] == day_of_month: #if the tweet was made today then update the count
            count += 1
        if tweet.created_at.timetuple()[2] < day_of_month: #if the tweet wasn't made today the loop breaks. this prevents prior month's tweets from being counted
            break
    return count
        
def tweet_count_hourly():
    current_time = time.ctime(time.time())
    day_of_month = time.gmtime()[2]
    current_minute_val = time.gmtime()[3]
    if current_minute_val == 0:
        print("Tweeting hourly update")
        api.update_status("So far Trump has tweeted " + str(count_tweets(day_of_month)) + " times! \n (" + current_time + ")!")
        print("Status tweeted")

def tweet_count_yesterday(): 
    yesterday_day_of_month = time.gmtime()[2] - 1
    return count_tweets(yesterday_day_of_month)

def tweet_count_midnight():
    current_time = time.ctime(time.time())
    yesterday_date = datetime.date.today() - datetime.timedelta(1)
    midnight = time.gmtime()[3] == 0 and time.gmtime()[4] == 0 and time.gmtime()[5] <= 15 #bool that is true when it is midnight
    if midnight:
        print("Tweeting midnight status")
        api.update_status("Yesterday (" + yesterday_date.strftime('%m/%d/%Y') + ") Trump tweeted " + str(tweet_count_yesterday()) + " times! \n (" + current_time + ")!")
        print("Status tweeted")

def tweet_oncommand():
    current_time = time.ctime(time.time())
    day_of_month = time.gmtime()[2]
    last_seen_id = read_last_id()
    if last_seen_id != 0:
        mentions = api.mentions_timeline(last_seen_id) #only mentions that haven't been seen yet
    else:
        mentions = api.mentions_timeline() #only mentions that haven't been seen yet
    for mention in reversed(mentions): #iterating through all unseen mentions
        user = mention.user.screen_name #twitter username
        last_seen_id = mention.id #updating last_seen_id
        if '#count' in mention.text:
            print("Count command made")
            api.update_status("@" + user + " Trump has tweeted " + str(count_tweets(day_of_month)) + " times so far today \n (" + current_time + ")!")
            write_last_id(str(last_seen_id))
            print("Status updated")
        if '#yesterday_count' in mention.text:
            print("Count command made")
            api.update_status("@" + user + " Trump has tweeted " + str(tweet_count_yesterday()) + " yesterday! \n today's date & time (" + current_time + ")")
            write_last_id(str(last_seen_id))
            print("Status updated")

def run():
    tweet_oncommand() #checking for new count commands
    tweet_count_hourly()
    tweet_count_midnight()

while True:
    run()
    time.sleep(15)

